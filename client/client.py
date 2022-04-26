import socket
import pickle
import threading
from server.request import Request, Message

class Client:
    '''
    A client which connects and sends requests to the server.
    Sends server's responses/notifications to the observers of the Client.
    '''
    def __init__(self, host='144.202.8.233', port=1234, buffer_size=1024):
        self.host = host # the server's host name or IP address
        self.port = port # the port used by the server
        self.buffer_size = buffer_size
        self.my_socket = socket.socket()
        self.my_socket.connect((self.host, self.port))
        self.observers = []
        thread = threading.Thread(target=self.receive_messages)
        thread.start()

    def set_observer(self, observer):
        '''
        Sets the observer to the given observer
        '''
        self.observers = [observer]
    
    def add_observer(self, observer):
        '''
        Adds the given observer to the list of observers
        '''
        self.observers.append(observer)

    def login(self, username, password):
        '''
        Request to log in the username with the password
        '''
        self.send_message(Message(Request.LOGIN, {
            'username': username,
            'password': password
        }))

    def logout(self, username):
        '''
        Log the user out of the system
        '''
        self.send_message(Message(Request.LOGOUT, {
            'username': username
        }))
    
    def register(self, username, password):
        '''
        Attempt to register the given username and password
        '''
        self.send_message(Message(Request.REGISTER, {
            'username': username,
            'password': password
        }))

    def update_game_state(self, board, game_mode, current_player, username):
        '''
        Update the state of the local game, so that we can continue the game if it is interrupted
        '''
        self.send_message(Message(Request.UPDATE_GAME_STATE, {
            'board': board,
            'game_mode': game_mode,
            'current_player': current_player,
            'username': username
        }))

    def remove_game_state(self, username):
        '''
        Remove whatever local game state is saved in the database.
        We do this once the game is terminated.
        '''
        self.send_message(Message(Request.REMOVE_GAME_STATE, {
            'username': username
        }))

    def get_game_state(self, username):
        '''
        Get the state of the last local game that was interrupted before terminating
        '''
        self.send_message(Message(Request.GET_GAME_STATE, {
            'username': username
        }))

    def get_leaderboard(self):
        '''
        Get the users with the top ten ELORatings
        '''
        self.send_message(Message(Request.LEADERBOARD, None))

    def update_settings(self, board_size, board_color, game_mode, username):
        '''
        Update the user's saved settings
        '''
        self.send_message(Message(Request.UPDATE_SETTINGS, {
            'board_size': board_size,
            'board_color': board_color,
            'game_mode': game_mode,
            'username': username
        }))
    
    def update_remote_game(self, username, move):
        '''
        Send a move to the opponent during a remote game
        '''
        self.send_message(Message(Request.UPDATE_REMOTE_GAME, {
            'username': username,
            'move': move
        }))

    def get_settings(self, username):
        '''
        Get the user's saved settings
        '''
        self.send_message(Message(Request.GET_SETTINGS, {
            'username': username
        }))

    def end_remote_game(self, username, player_disrupted_game):
        '''
        End a remote game.
        Unmatch the user with their opponent.
        Also notify the opponent if the user has left the game before it was terminated.
        '''
        self.send_message(Message(Request.END_REMOTE_GAME, {
            'username': username,
            'player_disrupted_game': player_disrupted_game
        }))

    def update_elo_rating(self, username, winner):
        '''
        Update the user's ELORating based on the winner of the game
        '''
        self.send_message(Message(Request.UPDATE_ELO_RATING, {
            'username': username,
            'winner': winner
        }))

    def get_online_players(self):
        '''
        Get all online players
        '''
        self.send_message(Message(Request.GET_ONLINE_PLAYERS, None))

    def request_game(self, username, opponent, board_size):
        '''
        Invite a user to play a remote game
        '''
        self.send_message(Message(Request.REQUEST_REMOTE_GAME, {
            'username': username,
            'opponent': opponent,
            'board_size': board_size
        }))

    def answer_game_request(self, username, opponent, remote_game_request_status):
        '''
        Response to a game invitation.
        This happens when the user accepts or declines an invitation to play.
        '''
        self.send_message(Message(Request.UPDATE_REMOTE_GAME_STATUS, {
            'username': username,
            'opponent': opponent,
            'response': remote_game_request_status
        }))

    def send_message(self, message):
        '''
        Send the given message to the server
        '''
        print(f"Sending message {message.message_type}, {message.body}")
        message_binary = pickle.dumps(message)
        self.my_socket.sendall(message_binary)

    def receive_messages(self):
        '''
        Handles any messages sent from the server
        '''
        while True:
            try:
                message_binary = self.my_socket.recv(self.buffer_size)
                message = pickle.loads(message_binary)
                self.update_observers(message)
            except OSError:
                break
    
    def update_observers(self, message):
        '''
        Send the observers a message from the server
        '''
        for observer in self.observers:
            observer.update(self, message=message)

    def disconnect(self):
        '''
        Disconnect the client
        '''
        self.my_socket.shutdown(socket.SHUT_RDWR)
        self.my_socket.close()