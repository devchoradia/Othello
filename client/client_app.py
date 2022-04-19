import tkinter as tk
from client.chat_client import ChatClient
from client.login_window import LoginWindow
from client.chat_window import ChatWindow

class ClientApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.client = ChatClient()

        self.withdraw()
        login_win = LoginWindow(self)
        login_win.focus_force()
        self.wait_window(login_win)

        if hasattr(login_win, 'username'):
            username = login_win.username
            chat_win = ChatWindow(self, username)
            chat_win.focus_force()
        else:
            self.destroy()