import socket
import pickle
import threading
from server.request import Request, Message

class Client:
    def __init__(self, host='127.0.0.1', port=1200, buffer_size=1024):
        self.host = host # the server's host name or IP address
        self.port = port # the port used by the server
        self.buffer_size = buffer_size
        self.my_socket = socket.socket()
        self.my_socket.connect((self.host, self.port))
        self.observers = []
        thread = threading.Thread(target=self.receive_messages)
        thread.start()

    def set_observer(self, observer):
        self.observers = [observer]
    
    def add_observer(self, observer):
        self.observers.append(observer)

    def login(self, username, password):
        self.send_message(Message(Request.LOGIN, {
            'username': username,
            'password': password
        }))
    
    def register(self, username, password):
        self.send_message(Message(Request.REGISTER, {
            'username': username,
            'password': password
        }))

    def update_game_state(self, board, game_mode, current_player, username):
        self.send_message(Message(Request.UPDATE_GAME_STATE, {
            'board': board,
            'game_mode': game_mode,
            'current_player': current_player,
            'username': username
        }))

    def remove_game_state(self, username):
        self.send_message(Message(Request.REMOVE_GAME_STATE, {
            'username': username
        }))

    def get_game_state(self, username):
        self.send_message(Message(Request.GET_GAME_STATE, {
            'username': username
        }))

    def get_leaderboard(self):
        self.send_message(Message(Request.LEADERBOARD, None))

    def update_settings(self, board_size, board_color, game_mode, username):
        self.send_message(Message(Request.UPDATE_SETTINGS, {
            'board_size': board_size,
            'board_color': board_color,
            'game_mode': game_mode,
            'username': username
        }))
    
    def update_remote_game(self, username, move):
        self.send_message(Message(Request.UPDATE_REMOTE_GAME, {
            'username': username,
            'move': move
        }))
    
    def request_opponent(self, username, board_size):
        self.send_message(Message(Request.REMOTE_PLAY, {
            'username': username,
            'board_size': board_size
        }))

    def get_settings(self, username):
        self.send_message(Message(Request.GET_SETTINGS, {
            'username': username
        }))

    def end_remote_game(self, username, player_disrupted_game):
        self.send_message(Message(Request.END_REMOTE_GAME, {
            'username': username,
            'player_disrupted_game': player_disrupted_game
        }))

    def update_elo_rating(self, username, winner):
        self.send_message(Message(Request.UPDATE_ELO_RATING, {
            'username': username,
            'winner': winner
        }))

    def send_message(self, message):
        print(f"Sending message {message.message_type}, {message.body}")
        message_binary = pickle.dumps(message)
        self.my_socket.sendall(message_binary)

    def receive_messages(self):
        while True:
            try:
                message_binary = self.my_socket.recv(self.buffer_size)
                message = pickle.loads(message_binary)
                self.update_observers(message)
            except OSError:
                break
    
    def update_observers(self, message):
        for observer in self.observers:
            observer.update(self, message=message)

    def disconnect(self):
        self.my_socket.shutdown(socket.SHUT_RDWR)
        self.my_socket.close()