from model.player import PLAYER_COLOR
import tkinter as tk
from abc import ABC, abstractmethod
import threading
import time

COLUMN_WIDTHS = [5, 7, 7]
ROW_HEIGHT = 2

# Renders the leaderboard
class LeaderboardView(ABC):
    def __init__(self, root, players, on_home):
        self.root = root
        self.players = players
        self.closed = tk.Variable()
        self.on_home = on_home
        self.widgets = []

    def display(self):
        self.add_title()
        self.add_column_labels()
        for row, player in enumerate(self.players):
            for col in range(3):
                column_values = [str(col+1), player[0], str(player[1])]
                frame = tk.Frame(padx=5, pady=5,relief=tk.RAISED, borderwidth=1, bg='white')
                frame.grid(row=row+2, column=col, sticky= tk.W+tk.E+tk.N+tk.S)
                tile = tk.Label(frame, borderwidth=1, width=COLUMN_WIDTHS[col], height=ROW_HEIGHT, text=column_values[col],bg="white", fg="black")
                tile.pack(ipadx=1, ipady=1, expand=True)
                self.widgets.append(frame)
        self.add_navigator()
    
    def add_navigator(self):
        home_button = tk.Button(self.root, text="Home", borderwidth=1, height=ROW_HEIGHT, bg="white", fg="black", \
            command=self.close)
        home_button.grid(row=len(self.players) + 2, columnspan=len(COLUMN_WIDTHS), sticky= tk.W+tk.E+tk.N+tk.S)
        self.widgets.append(home_button)
        
    def add_title(self):
        label = tk.Label(relief=tk.RAISED, borderwidth=1, width=20, height=ROW_HEIGHT, font=("Arial", 25), text="Leaderboard",bg="white", fg="black")
        label.grid(row=0, columnspan=len(COLUMN_WIDTHS), sticky= tk.W+tk.E+tk.N+tk.S)
        self.widgets.append(label)

    def add_column_labels(self):
        # Rank
        frame = tk.Frame(relief=tk.RAISED, borderwidth=1, bg='gray')
        frame.grid(row=1, column=0, sticky= tk.W+tk.E+tk.N+tk.S)
        tile = tk.Label(frame, borderwidth=1, width=COLUMN_WIDTHS[0], height=ROW_HEIGHT, text="Rank",bg="gray")
        tile.pack(expand=True)
        self.widgets.append(frame)
        # Username
        frame = tk.Frame(relief=tk.RAISED, borderwidth=1, bg='gray')
        frame.grid(row=1, column=1, sticky= tk.W+tk.E+tk.N+tk.S)
        tile = tk.Label(frame, borderwidth=1, width=COLUMN_WIDTHS[1], height=ROW_HEIGHT, text="Player",bg="gray")
        tile.pack(expand=True)
        self.widgets.append(frame)
        # ELORating
        frame = tk.Frame(relief=tk.RAISED, borderwidth=1, bg='gray')
        frame.grid(row=1, column=2, sticky= tk.W+tk.E+tk.N+tk.S)
        tile = tk.Label(frame, borderwidth=1, width=COLUMN_WIDTHS[2], height=ROW_HEIGHT, text="Rating",bg="gray")
        tile.pack(expand=True)
        self.widgets.append(frame)

    def close(self):
        for widget in self.widgets:
            widget.destroy()
        self.on_home()