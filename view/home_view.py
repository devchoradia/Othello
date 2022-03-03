import tkinter as tk
from abc import ABC, abstractmethod
from model.views import Views, VIEW_TITLES

ROW_HEIGHT = 2
COLUMNS = [Views.GAME, Views.LEADERBOARD, Views.SETTINGS]

# Renders the home page
class HomeView(ABC):
    def __init__(self, on_select_page, root):
        self.root = root
        self.frame = tk.Frame(root)
        self.on_select_page = on_select_page
        self.closed = tk.Variable()

    def display(self):
        self.frame.configure(background="white")
        self.add_title()
        for row, column in enumerate(COLUMNS):
            button = tk.Button(self.frame, text=VIEW_TITLES[column], borderwidth=1, width=40, height=ROW_HEIGHT, command=lambda col=column: self.on_click(col))
            button.pack(padx=5, pady=5)
        self.frame.pack()
    
    def add_title(self):
        label = tk.Label(self.frame, relief=tk.RAISED, borderwidth=1, width=40, height=ROW_HEIGHT, font=("Arial", 25), text="Home",bg="white", fg="black")
        label.pack()

    def on_click(self, view):
        self.frame.destroy()
        self.on_select_page(view)


