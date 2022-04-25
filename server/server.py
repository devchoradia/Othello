import socket
import pickle
import threading
from server.database_client import DatabaseClient, LOGIN_RESULT, REGISTER_RESULT
from datetime import datetime
from enum import Enum
from model.player.player import Player
from model.game_mode import REMOTE_GAME_REQUEST_STATUS
import schedule
import time
from server.request import Request, Message

class Server:
    def __init__(self, host='127.0.0.1', port=1200, buffer_size=1024):
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
        with socket.socket() as my_socket:
            my_socket.bind((self.host, self.port))
            my_socket.listen()
            print('Server started')
            thread = threading.Thread(target=self.run_scheduled_tasks, args=())
            thread.start()

            while True:
                conn, address = my_socket.accept()
                print(f'Connected by {address}')
                self.clients.append(conn)
                thread = threading.Thread(target=self.handle_client, args=(conn,))
                thread.start()

    def handle_client(self, conn):
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
            # text = f'{username} has disconnected from the chat'

    def broadcast_message(self, text):
        message = ChatMessage(text)
        message_binary = pickles.dumps(message)
        for client in self.clients:
            client.sendall(message_binary)
        
    def send_message(self, result, conn):
        if result is not None:
            print(f'Sending message {result.message_type}, {result.body}')
            result_binary = pickle.dumps(result)
            conn.sendall(result_binary)

    def on_login(self, username, password, conn):
        result, body = self.database_client.login(username, password)
        if result == LOGIN_RESULT.SUCCESS:
            self.remote_connections[username] = conn
        return (result, body)

    def on_register(self, username, password, conn):
        result, body = self.database_client.register_user(username, password)
        if result == REGISTER_RESULT.SUCCESS:
            self.remote_connections[username] = conn
        return (result, body)

    def get_leaderboard(self):
        return self.database_client.get_leaderboard()

    def remove_game_state(self, username):
        return self.database_client.remove_game_state(username)

    def update_game_state(self, board, game_mode, current_player, username):
        return self.database_client.update_game_state(board, game_mode, current_player, username)

    def get_game_state(self, username):
        return self.database_client.get_game_state(username)

    def update_settings(self, board_size, board_color, game_mode, username):
        self.database_client.update_settings(board_size, board_color, game_mode, username)

    def get_settings(self, username):
        return self.database_client.get_settings(username)

    def get_online_players(self):
        online_players = list(self.remote_connections.keys())
        return self.database_client.get_ratings(online_players)

    def handle_remote_play(self, username, board_size, conn):
        print(f'Current remote game queue: {self.remote_queue}')
        self.remote_connections[username] = conn
        dt = datetime.now()
        if len(self.remote_queue) == 0:
            self.remote_queue.append((username, board_size, dt))
            return
        self.remote_queue.append((username, board_size, dt))
        # Look for someone looking for same board size
        schedule.every(2).seconds.do(lambda u=username, s=board_size: self.check_remote_queue(u, s)).tag(username)

    def run_scheduled_tasks(self):
        while True:
            schedule.run_pending()
            time.sleep(1)

    def check_remote_queue(self, username, board_size):
        print(f'Current remote game queue: {self.remote_queue}')
        now = datetime.now()
        queue_index = len(self.remote_queue)
        if username in self.remote_pairs:
            schedule.clear(username)
            return
        for index, (opponent, opp_board_size, dt) in enumerate(self.remote_queue):
            if opponent == username:
                queue_index = index
                continue
            time_waited = now - dt
            games_match = board_size == opp_board_size
            if time_waited.total_seconds() >= 45 or games_match:
                print(f'Matching {username} with {opponent}')
                if index < queue_index:
                    self.match_opponents(username, opponent, opp_board_size)
                else:
                    self.match_opponents(username, opponent, board_size)
                del self.remote_queue[index]
                current_user = next((x for x in self.remote_queue if x[0] == username), None)
                if current_user is not None:
                    self.remote_queue.remove(current_user)
                return
    
    def match_opponents(self, username, opponent, board_size):
        self.remote_pairs[username] = opponent
        self.remote_pairs[opponent] = username
        self.player_colors[opponent] = Player.BLACK
        self.player_colors[username] = Player.WHITE
        if username in self.game_requests:
            del self.game_requests[username]
        if opponent in self.game_requests:
            del self.game_requests[opponent]

    def handle_remote_game_update(self, username, move):
        opponent = self.remote_connections[self.remote_pairs[username]]
        self.send_message(Message(Request.UPDATE_REMOTE_GAME, move), opponent)

    def end_remote_game(self, username, player_disrupted_game=False):
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
        for requester, (board_size, opponent) in self.game_requests.items():
            if opponent == username:
                self.send_message(Message(Request.UPDATE_REMOTE_GAME_STATUS, REMOTE_GAME_REQUEST_STATUS.DISCONNECTED, None, None, None))
        schedule.clear(username)
    
    def update_elo_rating(self, username, winner):
        K = 32 # K-FACTOR
        if username in self.remote_pairs and username in self.player_colors:
            player_color = self.player_colors[username]
            opponent = self.remote_pairs[username]
            if opponent not in self.player_colors:
                print(f"Could not find player color saved for opponent {opponent}")
                return
            opponent_rating = int(self.database_client.get_rating(opponent)[0][0])
            user_rating = int(self.database_client.get_rating(username)[0][0])
            r1 = pow(10, user_rating/400)
            r2 = pow(10, opponent_rating/400)
            e1 = r1 / (r1 + r2)
            e2 = r2 / (r1 + r2)
            s1 = 0.5 # DRAW
            if player_color == winner: # USER WON
                s1 = 1
            elif winner == self.player_colors[opponent]: # USER LOST
                s1 = 0
            new_rating = round(user_rating + K*(s1-e1))
            result = self.database_client.update_rating(new_rating, username)
            print(result)
            print(self.database_client.get_rating(username))
            print(f"Updated ELORating from {user_rating} to {new_rating} for {username}")
            return new_rating
        print(f"Could not find {username} in remote pairs and/or player_colors")

    def notify_opponent_disconnected(self, user):
        if user in self.remote_connections:
            self.send_message(Message(Request.OPPONENT_DISCONNECTED, "Opponent disconnected from the game"), self.remote_connections[user])

    def request_remote_game(self, username, opponent, board_size, conn):
        if username not in self.remote_connections:
            print(f"Remote connections was missing user {username}")
            self.remote_connections[username] = conn
        if opponent not in self.remote_connections:
            return REMOTE_GAME_REQUEST_STATUS.DISCONNECTED, None, None, None
        self.game_requests[username] = (board_size, opponent)
        self.send_message(Message(Request.REQUEST_REMOTE_GAME, (username, board_size, Player.WHITE)), self.remote_connections[opponent])

    def update_remote_game_status(self, remote_game_request_status, username, opponent, conn):
        if username not in self.remote_connections:
            print(f"Remote connections was missing user {username}")
            self.remote_connections[username] = conn
        if opponent not in self.remote_connections or opponent not in self.game_requests:
            return REMOTE_GAME_REQUEST_STATUS.DISCONNECTED, None, None, None
        board_size = self.game_requests[opponent][0]
        if remote_game_request_status == REMOTE_GAME_REQUEST_STATUS.ACCEPTED:
            self.match_opponents(opponent, username, self.game_requests[opponent][0])
        self.send_message(Message(Request.UPDATE_REMOTE_GAME_STATUS, (remote_game_request_status, username, board_size, Player.BLACK)), self.remote_connections[opponent])
    
    def logout(self, username):
        if username in self.remote_connections:
            del self.remote_connections[username]

    def compute_result(self, message, conn):
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
            return Message(Request.UPDATE_GAME_STATE, self.update_game_state(body['board'], body['game_mode'], body['current_player'], body['username']))
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
            error = self.update_remote_game_status(body['response'], body['username'], body['opponent'], conn)
            if error is not None:
                return Message(Request.UPDATE_REMOTE_GAME_STATUS, error)
        elif message_type == Request.UPDATE_REMOTE_GAME:
            self.handle_remote_game_update(body['username'], body['move'])
        elif message_type == Request.END_REMOTE_GAME:
            self.end_remote_game(body['username'], body['player_disrupted_game'])
        elif message_type == Request.UPDATE_ELO_RATING:
            return Message(Request.UPDATE_ELO_RATING, self.update_elo_rating(body['username'], body['winner']))
        elif message_type == Request.LOGOUT:
            self.logout(body['username'])
        return None

    class ChatMessage:
        def __init(self, text):
            self.text = text

