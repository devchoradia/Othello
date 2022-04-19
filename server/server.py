import socket
import pickle
import threading
from server.database_client import DatabaseClient
from datetime import datetime
from enum import Enum
from model.player.player import Player
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
        self.remote_queue = []

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
                result = self.compute_result(message, conn)
                self.send_message(result, conn)
            print('Client disconnected')
            self.clients.remove(conn)
            if conn in self.remote_connections.values():
                user = list(self.remote_connections.keys())[list(self.remote_connections.values()).index(conn)]
                print(f'Deleting connection {user} from remote_connections')
                if username in self.remote_connections:
                    del self.remote_connections[username]
                self.end_remote_game(user)
            # text = f'{username} has disconnected from the chat'

    def broadcast_message(self, text):
        message = ChatMessage(text)
        message_binary = pickles.dumps(message)
        for client in self.clients:
            client.sendall(message_binary)
        
    def send_message(self, result, conn):
        if result is not None:
            print(f'Sending message ({result.message_type}, {result.body}) to {conn}')
            result_binary = pickle.dumps(result)
            conn.sendall(result_binary)

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

    def update_settings(self, board_size, board_color, game_mode, username):
        self.database_client.update_settings(board_size, board_color, game_mode, username)

    def get_settings(self, username):
        return self.database_client.get_settings(username)

    def handle_remote_play(self, username, board_size, conn):
        self.remote_connections[username] = conn
        dt = datetime.now()
        if len(self.remote_queue) == 0:
            print("empty remote queue")
            self.remote_queue.append((username, board_size, dt))
            return
        self.remote_queue.append((username, board_size, dt))
        print("Foudn unempty remote queue")
        print(self.remote_queue)
        # Look for someone looking for same board size
        schedule.every(2).seconds.do(lambda u=username, s=board_size: self.check_remote_queue(u, s)).tag(username)
        thread = threading.Thread(target=self.run_scheduled_tasks, args=())
        thread.start()

    def run_scheduled_tasks(self):
        while True:
            schedule.run_pending()
            time.sleep(1)

    def check_remote_queue(self, username, board_size):
        print("Checking remote queue")
        print(self.remote_queue)
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
                print("got match")
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
        print(self.remote_pairs)
        if opponent == self.remote_pairs.get(username, None) and username == self.remote_pairs.get(opponent, None):
            print("Skipping match")
            return
        self.remote_pairs[username] = opponent
        self.remote_pairs[opponent] = username
        self.send_message(Message(Request.REMOTE_PLAY, (opponent, board_size, Player.BLACK)), self.remote_connections[username])
        self.send_message(Message(Request.REMOTE_PLAY, (username, board_size, Player.WHITE)), self.remote_connections[opponent])

    def handle_remote_game_update(self, username, move):
        opponent = self.remote_connections[self.remote_pairs[username]]
        self.send_message(Message(Request.UPDATE_REMOTE_GAME, move), opponent)

    def end_remote_game(self, username, player_disrupted_game=False):
        user_in_queue = next((x for x in self.remote_queue if x[0] == username), None)
        if user_in_queue is not None:
            self.remote_queue.remove(user_in_queue)
        if username in self.remote_pairs:
            opponent = self.remote_pairs[username]            
            del self.remote_pairs[username]
            if opponent in self.remote_pairs and self.remote_pairs[opponent] == username:
                if player_disrupted_game:
                    self.notify_opponent_disconnected(opponent)
                del self.remote_pairs[opponent]
        schedule.clear(username)

    def notify_opponent_disconnected(self, user):
        if user in self.remote_connections:
            self.send_message(Message(Request.OPPONENT_DISCONNECTED, "Opponent disconnected from the game"), self.remote_connections[user])

    def compute_result(self, message, conn):
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
        elif message_type == Request.UPDATE_SETTINGS:
            self.update_settings(body['board_size'], body['board_color'], body['game_mode'], body['username'])
        elif message_type == Request.GET_SETTINGS:
            return Message(Request.GET_SETTINGS, self.get_settings(body['username']))
        elif message_type == Request.REMOTE_PLAY:
            return self.handle_remote_play(body['username'], body['board_size'], conn)
        elif message_type == Request.UPDATE_REMOTE_GAME:
            self.handle_remote_game_update(body['username'], body['move'])
        elif message_type == Request.END_REMOTE_GAME:
            self.end_remote_game(body['username'], body['player_disrupted_game'])
        return None

    class ChatMessage:
        def __init(self, text):
            self.text = text

