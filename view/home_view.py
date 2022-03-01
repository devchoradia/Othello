import tkinter as tk
from abc import ABC, abstractmethod
from model.views import Views, VIEW_TITLES

ROW_HEIGHT = 2
COLUMNS = [Views.GAME, Views.LEADERBOARD, Views.SETTINGS]

# Renders the home page
class HomeView(ABC):
    def __init__(self, on_select_page):
        self.root = tk.Tk()
        self.on_select_page = on_select_page
        self.closed = tk.Variable()

    def display(self):
        self.root.geometry("400x400")
        self.root.configure(background="white")
        self.add_title()
        for row, column in enumerate(COLUMNS):
            button = tk.Button(self.root, text=VIEW_TITLES[column], borderwidth=1, width=40, height=ROW_HEIGHT, command=lambda col=column: self.on_click(col))
            button.pack(padx=5, pady=5)
        self.root.mainloop()
    
    def add_title(self):
        label = tk.Label(self.root, relief=tk.RAISED, borderwidth=1, width=40, height=ROW_HEIGHT, font=("Arial", 25), text="Home",bg="white", fg="black")
        label.pack()

    def on_click(self, view):
        self.root.destroy()
        self.on_select_page(view)

    def close(self):
        self.root.destroy()
