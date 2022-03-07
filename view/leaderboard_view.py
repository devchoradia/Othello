from model.player import PLAYER_COLOR
import tkinter as tk
from view.abstract_page_view import AbstractPageView, STICKY
import threading
import time

COLUMNS = ["Rank", "Player", "Rating"]
COLUMN_WIDTHS = [5, 7, 7]
ROW_HEIGHT = 2

# Renders the leaderboard
class LeaderboardView(AbstractPageView):
    def __init__(self, root, players, on_home):
        super().__init__(root, "Leaderboard", len(COLUMN_WIDTHS), on_home)
        self.players = players
        self.closed = tk.Variable()

    def display(self):
        self.add_title()
        self.add_column_labels()
        for row, player in enumerate(self.players):
            for col in range(3):
                column_values = [str(col+1), player[0], str(player[1])]
                frame = tk.Frame(padx=5, pady=5,relief=tk.RAISED, borderwidth=1, bg='white')
                frame.grid(row=row+2, column=col, sticky=STICKY)
                tile = tk.Label(frame, borderwidth=1, width=COLUMN_WIDTHS[col], height=ROW_HEIGHT, text=column_values[col],bg="white", fg="black")
                tile.pack(ipadx=1, ipady=1, expand=True)
                self.widgets.append(frame)
        self.add_navigator(len(self.players)+2)

    def add_column_labels(self):
        for index, column in enumerate(COLUMNS):
            frame = tk.Frame(relief=tk.RAISED, borderwidth=1, bg='gray')
            frame.grid(row=1, column=index, sticky=STICKY)
            tile = tk.Label(frame, borderwidth=1, width=COLUMN_WIDTHS[0], height=ROW_HEIGHT, text=column,bg="gray")
            tile.pack(expand=True)
            self.widgets.append(frame)

    def close(self):
        for widget in self.widgets:
            widget.destroy()
        self.on_home()