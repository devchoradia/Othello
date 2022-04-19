import tkinter as tk
from tkinter import messagebox

class LoginWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Login')

        self.resizable(0, 0)

        # username
        self.username_label = tk. Label(self, text='Username:')
        self.username_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.username_entry = tk.Entry(self)
        self.username_entry.grid(row=0, column=1, sticky=tk.E, padx=5, pady=5)

        # login button
        self.login_button = tk.Button(self, text='Connec t', command=self.login)
        self.login_button.grid(row=1, column=1, sticky=tk.E, padx=5, pady=5)

    def login(self):
        self.username = self.username_entry.get()
        self.destroy()