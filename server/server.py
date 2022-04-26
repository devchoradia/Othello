import pickle
import socket
import threading

from model.game_mode import REMOTE_GAME_REQUEST_STATUS
from model.player.player import Player
from server.database_client import DatabaseClient, LOGIN_RESULT, REGISTER_RESULT
from server.request import Request, Message


class Server:
    '''
    Reversi Game Server
    Handles all client requests and database queries
    '''

    def __init__(self, host='127.0.0.1', port=1201, buffer_size=1024):
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self.clients = []
        self.database_client = DatabaseClient()
        self.remote_connections = {}
        self.remote_pairs = {}
        self.game_requests = {}
        self.player_colors = {}

    def start(self):
        '''
        Begin running the server
        '''
        with socket.socket() as my_socket:
            my_socket.bind((self.host, self.port))
            my_socket.listen()
            print('Server started')

            while True:
                conn, address = my_socket.accept()
                print(f'Connected by {address}')
                self.clients.append(conn)
                thread = threading.Thread(target=self.handle_client, args=(conn,))
                thread.start()

    def handle_client(self, conn):
        '''
        Begin a thread to handle the client
        '''
        with conn:
            while True:
                message_binary = conn.recv(self.buffer_size)
                if not message_binary:
                    break
                message = pickle.loads(message_binary)
                print(f'Received message: ({message.message_type}, {message.body})')
                result = self.compute_result(message, conn)
                self.send_message(result, conn)
            print('Client disconnected')
            self.clients.remove(conn)
            if conn in self.remote_connections.values():
                user = list(self.remote_connections.keys())[list(self.remote_connections.values()).index(conn)]
                player_left_game = user in self.remote_connections and user in self.remote_pairs and user in self.player_colors
                if user in self.remote_connections:
                    del self.remote_connections[user]
                self.end_remote_game(user, player_left_game)
                self.logout(user)

    def send_message(self, result, conn):
        '''
        Send a message to the given client connection
        '''
        if result is not None:
            print(f'Sending message: {result.message_type}, {result.body}')
            result_binary = pickle.dumps(result)
            conn.sendall(result_binary)

    def on_login(self, username, password, conn):
        '''
        Log in the user and return the login result
        '''
        result, body = self.database_client.login(username, password)
        if result == LOGIN_RESULT.SUCCESS:
            self.remote_connections[username] = conn
        return (result, body)

    def on_register(self, username, password, conn):
        '''
        Attempt to register the username/password and return the result
        '''
        result, body = self.database_client.register_user(username, password)
        if result == REGISTER_RESULT.SUCCESS:
            self.remote_connections[username] = conn
        return (result, body)

    def get_leaderboard(self):
        '''
        Get the users with the top 10 ELORatings
        '''
        return self.database_client.get_leaderboard()

    def remove_game_state(self, username):
        '''
        Remove the state of the local game saved in the database.
        This happens when the game is finished so we don't need to be able to continue it
        '''
        return self.database_client.remove_game_state(username)

    def update_game_state(self, board, game_mode, current_player, username):
        '''
        Update the last game state for the user's locally played game.
        This happens to handle exceptions and interruptions.
        When the user starts the game later, we can continue from here.
        '''
        return self.database_client.update_game_state(board, game_mode, current_player, username)

    def get_game_state(self, username):
        '''
        Return the current game state for the given user.
        This is the state of the game that was last played locally before being interrupted.
        '''
        return self.database_client.get_game_state(username)

    def update_settings(self, board_size, board_color, game_mode, username):
        '''
        Update the user's preferred game settings
        '''
        self.database_client.update_settings(board_size, board_color, game_mode, username)

    def get_settings(self, username):
        '''
        Get the user's preferred game settings
        '''
        return self.database_client.get_settings(username)

    def get_online_players(self):
        '''
        Get all players currently online
        '''
        online_players = list(self.remote_connections.keys())
        return self.database_client.get_ratings(online_players)

    def match_opponents(self, player_1, player_2, board_size):
        '''
        Match the two given opponents.
        player_1 will be the Black player.
        player_2 will be White.
        '''
        self.remote_pairs[player_1] = player_2
        self.remote_pairs[player_2] = player_1
        self.player_colors[player_1] = Player.BLACK
        self.player_colors[player_2] = Player.WHITE
        if player_1 in self.game_requests:
            del self.game_requests[player_1]
        if player_2 in self.game_requests:
            del self.game_requests[player_2]

    def handle_remote_game_update(self, username, move):
        '''
        Updates the opponent about the user's move in the game
        '''
        opponent = self.remote_connections[self.remote_pairs[username]]
        self.send_message(Message(Request.UPDATE_REMOTE_GAME, move), opponent)

    def end_remote_game(self, username, player_disrupted_game=False):
        '''
        End the current remote game for the user.
        Unmatch the player and opponent, and notify the opponent if the player abandoned the game while it was still playing.
        '''
        if username in self.remote_pairs:
            opponent = self.remote_pairs[username]
            del self.remote_pairs[username]
            if opponent in self.remote_pairs and self.remote_pairs[opponent] == username:
                if player_disrupted_game:
                    self.notify_opponent_disconnected(opponent)
                del self.remote_pairs[opponent]
        if username in self.player_colors:
            del self.player_colors[username]
        if username in self.game_requests:
            del self.game_requests[username]

    def update_elo_rating(self, username, winner):
        '''
        Update the ELORating for the user, given the winner of the game.
        Algorithm:
        * Initial ratings: r(1) and r(2) for player 1 and player 2
        * Transformed ratings:
            R(1) = 10r(1)/400
            R(2) = 10r(2)/400
        * Expected scores:
            E(1) = R(1) / (R(1) + R(2))
            E(2) = R(2) / (R(1) + R(2))
        * Results:
            S(1) = 1 if player 1 wins / 0.5 if draw / 0 if player 2 wins
            S(2) = 0 if player 1 wins / 0.5 if draw / 1 if player 2 wins
        * Updated ELORatings:
            r'(1) = r(1) + K * (S(1) – E(1))
            r'(2) = r(2) + K * (S(2) – E(2))

        * Implemented algorithm based on this guide:
            https://metinmediamath.wordpress.com/2013/11/27/how-to-calculate-the-elo-rating-including-example/
        '''
        K = 32  # K-FACTOR
        if username in self.remote_pairs and username in self.player_colors:
            player_color = self.player_colors[username]
            opponent = self.remote_pairs[username]
            if opponent not in self.player_colors:
                print(f"Could not find player color saved for opponent {opponent}")
                return
            opponent_rating = int(self.database_client.get_rating(opponent)[0][0])
            user_rating = int(self.database_client.get_rating(username)[0][0])
            r1 = pow(10, user_rating / 400)
            r2 = pow(10, opponent_rating / 400)
            e1 = r1 / (r1 + r2)
            e2 = r2 / (r1 + r2)
            s1 = 0.5  # DRAW
            if player_color == winner:  # USER WON
                s1 = 1
            elif winner == self.player_colors[opponent]:  # USER LOST
                s1 = 0
            new_rating = round(user_rating + K * (s1 - e1))
            result = self.database_client.update_rating(new_rating, username)
            print(result)
            print(self.database_client.get_rating(username))
            print(f"Updated ELORating from {user_rating} to {new_rating} for {username}")
            return new_rating
        print(f"Could not find {username} in remote pairs and/or player_colors")

    def notify_opponent_disconnected(self, user):
        '''
        Notifies the user's opponent that the user has disconnected from the ongoing remote game
        '''
        if user in self.remote_connections:
            self.send_message(Message(Request.OPPONENT_DISCONNECTED, "Opponent disconnected from the game"),
                              self.remote_connections[user])

    def request_remote_game(self, username, opponent, board_size, conn):
        '''
        Notify the 'opponent' that the user has requested to play a game
        '''
        if username not in self.remote_connections:
            print(f"Remote connections was missing user {username}")
            self.remote_connections[username] = conn
        if opponent not in self.remote_connections:
            return REMOTE_GAME_REQUEST_STATUS.DISCONNECTED, opponent, None, None
        self.game_requests[username] = (board_size, opponent)
        self.send_message(Message(Request.REQUEST_REMOTE_GAME, (username, board_size, Player.WHITE)),
                          self.remote_connections[opponent])

    def update_remote_game_status(self, remote_game_request_status, username, opponent, conn):
        '''
        Handles responses to remote game requests.
        This is called when the requestee declines or accepts and invitation to play.
        '''
        if username not in self.remote_connections:
            print(f"Remote connections was missing user {username}")
            self.remote_connections[username] = conn
        if opponent not in self.remote_connections or opponent not in self.game_requests:
            self.notify_opponent_disconnected(username)
            return
        board_size = self.game_requests[opponent][0]
        if remote_game_request_status == REMOTE_GAME_REQUEST_STATUS.ACCEPTED:
            self.match_opponents(opponent, username, self.game_requests[opponent][0])
        self.send_message(Message(Request.UPDATE_REMOTE_GAME_STATUS,
                                  (remote_game_request_status, username, board_size, Player.BLACK)),
                          self.remote_connections[opponent])

    def logout(self, username):
        '''
        Log the user out of the system.
        They no longer will appear on "online player" lists
        '''
        if username in self.remote_connections:
            del self.remote_connections[username]

    def compute_result(self, message, conn):
        '''
        Handles a message from a client, based on the Request type.
        Optionally returns a Message to send to the client.
        '''
        message_type = message.message_type
        body = message.body
        if message_type == Request.LOGIN:
            return Message(Request.LOGIN, self.on_login(body['username'], body['password'], conn))
        elif message_type == Request.REGISTER:
            return Message(Request.REGISTER, self.on_register(body['username'], body['password'], conn))
        elif message_type == Request.GET_GAME_STATE:
            return Message(Request.GET_GAME_STATE, self.get_game_state(body['username']))
        elif message_type == Request.REMOVE_GAME_STATE:
            return Message(Request.REMOVE_GAME_STATE, self.remove_game_state(body['username']))
        elif message_type == Request.UPDATE_GAME_STATE:
            return Message(Request.UPDATE_GAME_STATE,
                           self.update_game_state(body['board'], body['game_mode'], body['current_player'],
                                                  body['username']))
        elif message_type == Request.LEADERBOARD:
            return Message(Request.LEADERBOARD, self.get_leaderboard())
        elif message_type == Request.UPDATE_SETTINGS:
            self.update_settings(body['board_size'], body['board_color'], body['game_mode'], body['username'])
        elif message_type == Request.GET_SETTINGS:
            return Message(Request.GET_SETTINGS, self.get_settings(body['username']))
        elif message_type == Request.GET_ONLINE_PLAYERS:
            return Message(Request.GET_ONLINE_PLAYERS, self.get_online_players())
        elif message_type == Request.REQUEST_REMOTE_GAME:
            error = self.request_remote_game(body['username'], body['opponent'], body['board_size'], conn)
            if error is not None:
                return Message(Request.UPDATE_REMOTE_GAME_STATUS, error)
        elif message_type == Request.UPDATE_REMOTE_GAME_STATUS:
            self.update_remote_game_status(body['response'], body['username'], body['opponent'], conn)
        elif message_type == Request.UPDATE_REMOTE_GAME:
            self.handle_remote_game_update(body['username'], body['move'])
        elif message_type == Request.END_REMOTE_GAME:
            self.end_remote_game(body['username'], body['player_disrupted_game'])
        elif message_type == Request.UPDATE_ELO_RATING:
            return Message(Request.UPDATE_ELO_RATING, self.update_elo_rating(body['username'], body['winner']))
        elif message_type == Request.LOGOUT:
            self.logout(body['username'])
        return None
