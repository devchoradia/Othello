from model.player import PLAYER_COLOR
import tkinter as tk
from abc import ABC, abstractmethod
import threading
import time

COLUMN_WIDTHS = [5, 7, 7]
ROW_HEIGHT = 2

# Renders the leaderboard
class LeaderboardView(ABC):
    def __init__(self, players, on_close):
        self.players = players
        self.root = tk.Tk()
        self.closed = tk.Variable()
        self.on_close = on_close

    def mainloop(self):
         self.root.mainloop()

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
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.root.mainloop()
    
    def add_title(self):
        label = tk.Label(relief=tk.RAISED, borderwidth=1, width=20, height=ROW_HEIGHT, font=("Arial", 25), text="Leaderboard",bg="white", fg="black")
        label.grid(row=0, columnspan=len(COLUMN_WIDTHS), sticky= tk.W+tk.E+tk.N+tk.S)

    def add_column_labels(self):
        # Rank
        frame = tk.Frame(relief=tk.RAISED, borderwidth=1, bg='gray')
        frame.grid(row=1, column=0, sticky= tk.W+tk.E+tk.N+tk.S)
        tile = tk.Label(frame, borderwidth=1, width=COLUMN_WIDTHS[0], height=ROW_HEIGHT, text="Rank",bg="gray")
        tile.pack(expand=True)
        # Username
        frame = tk.Frame(relief=tk.RAISED, borderwidth=1, bg='gray')
        frame.grid(row=1, column=1, sticky= tk.W+tk.E+tk.N+tk.S)
        tile = tk.Label(frame, borderwidth=1, width=COLUMN_WIDTHS[1], height=ROW_HEIGHT, text="Player",bg="gray")
        tile.pack(expand=True)
        # ELORating
        frame = tk.Frame(relief=tk.RAISED, borderwidth=1, bg='gray')
        frame.grid(row=1, column=2, sticky= tk.W+tk.E+tk.N+tk.S)
        tile = tk.Label(frame, borderwidth=1, width=COLUMN_WIDTHS[2], height=ROW_HEIGHT, text="Rating",bg="gray")
        tile.pack(expand=True)

    def close(self):
        self.root.destroy()
        self.on_close()