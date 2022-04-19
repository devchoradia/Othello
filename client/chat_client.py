import socket
import pickle
import threading
from chat_message import ChatMessage

class ChatClient:
    def __init__(self, host='144.202.8.233', port=1234, buffer_size=1024):
        self.host = host # the server's host name or IP address
        self.port = port # the port used by the server
        self.buffer_size = buffer_size

    def set_observer(self, observer):
        self.observer = observer

    def connect(self, username):
        self.username = username
        self.my_socket = socket.socket()
        self.my_socket.connect((self.host, self.port))
        print('Client connected')

        # Send the username to the server
        self.my_socket.sendall(username.encode('utf-8'))

        thread = threading.Thread(target=self.receive_messages)
        thread.start()

    def send_message(self, text):
        message = ChatMessage(text)
        message_binary = pickle.dumps(message)
        self.my_socket.sendall(message_binary)

    def receive_messages(self):
        while True:
            try:
                message_binary = self.my_socket.recv(self.buffer_size)
                message = pickle.loads(message_binary)
                if self.observer:
                    self.observer.display_message(message)
            except OSError:
                break

    def disconnect(self):
        self.my_socket.shutdown(socket.SHUT_RDWR)
        self.my_socket.close()