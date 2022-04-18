import socket
import pickle
import threading
from server.database_client import DatabaseClient
from enum import Enum

class Server:
    def __init__(self, host='127.0.0.1', port=1201, buffer_size=1024):
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self.clients = []
        self.database_client = DatabaseClient()

    def start(self):
        with socket.socket() as my_socket:
            my_socket.bind((self.host, self.port))
            my_socket.listen()
            print('Server started')

            while True:
                conn, address = my_socket.accept()
                print(f'Connected by {address}')

                # Read the username
                # username = conn.recv(self.buffer_size)
                # print(username)
                # username = username.decode('utf-8')
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
                print(f'Received message: {message}')
                result = self.compute_result(message)
                if result is not None:
                    result_binary = pickle.dumps(result)
                    conn.sendall(result_binary)
                print('Client disconnected')
            self.clients.remove(conn)
            # text = f'{username} has disconnected from the chat'
            print(text)

    def broadcast_message(self, text):
        message = ChatMessage(text)
        message_binary = pickles.dumps(message)
        for client in self.clients:
            client.sendall(message_binary)

    def on_login(self, username, password):
        return self.database_client.login(username, password)

    def on_register(self, username, password):
        return self.database_client.register_user(username, password)

    def get_leaderboard(self):
        return self.database_client.get_leaderboard()

    def remove_game_state(self, username):
        return self.database_client.remove_game_state(username)

    def update_game_state(self, board, game_mode, current_player, username):
        return self.database_client.update_game_state(board, game_mode, current_player, username)

    def get_game_state(self, username):
        return self.database_client.get_game_state(username)

    def compute_result(self, message):
        message_type = message.message_type
        body = message.body
        print(body)
        if message_type == Request.LOGIN:
            return Message(Request.LOGIN, self.on_login(body['username'], body['password']))
        elif message_type == Request.REGISTER:
            return Message(Request.REGISTER, self.on_register(body['username'], body['password']))
        elif message_type == Request.GET_GAME_STATE:
            return Message(Request.GET_GAME_STATE, self.get_game_state(body['username']))
        elif message_type == Request.REMOVE_GAME_STATE:
            return Message(Request.REMOVE_GAME_STATE, self.remove_game_state(body['username']))
        elif message_type == Request.UPDATE_GAME_STATE:
            return Message(Request.UPDATE_GAME_STATE, self.update_game_state(body['board'], body['game_mode'], body['current_player'], body['username']))
        elif message_type == Request.LEADERBOARD:
            return Message(Request.LEADERBOARD, self.get_leaderboard())
        return None

    class ChatMessage:
        def __init(self, text):
            self.text = text

class Request(Enum):
    LOGIN = "login"
    REGISTER = "register"
    REMOVE_GAME_STATE = "remove game state"
    UPDATE_GAME_STATE = "update game state"
    GET_GAME_STATE = "get game state"
    LEADERBOARD = "leaderboard"

class Message:
    def __init__(self, message_type: Request, body):
        self.message_type = message_type
        self.body = body
