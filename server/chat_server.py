import socket
import pickle
import threading
from chat_message import ChatMessage

class ChatServer:
    def __init__(self, host='0.0.0.0', port=1234, buffer_size=1024):
        self.clients = []
        self.host = host  # the server's host name or IP address
        self.port = port  # the port used by the server
        self.buffer_size = buffer_size

    def start(self):
        with socket.socket() as my_socket:
            my_socket.bind((self.host, self.port))
            my_socket.listen()
            print('Server started')

            while True:
                conn, address = my_socket.accept()
                print(f'Connected by {address}')

                # Read the username
                username = conn.recv(1024)
                username = username.decode('utf-8')
                text = f'{username} has joined the chat'
                print(text)
                self.broadcast_message(text)

                self.clients.append(conn)

                thread = threading.Thread(target=self.handle_client, args=(conn, username))
                thread.start()

    def handle_client(self, conn, username):
        with conn:
            while True:
                message_binary = conn.recv(self.buffer_size)
                if not message_binary:
                    break
                message = pickle.loads(message_binary)
                print(f'Received message: {message.text}')

                text = f'{username} said: {message.text}'
                self.broadcast_message(text)
            self.clients.remove(conn)
            text = f'{username} has disconnected from the chat'
            print(text)
            self.broadcast_message(text)

    def broadcast_message(self, text):
        message = ChatMessage(text)
        message_binary = pickle.dumps(message)
        for client in self.clients:
            client.sendall(message_binary)
