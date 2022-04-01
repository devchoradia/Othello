from model.player.player import PLAYER_COLOR
import tkinter as tk
from view.abstract_page_view import AbstractPageView, STICKY
import threading
from model.views import Views
import time

COLUMNS = ["Rank", "Player", "Rating"]
COLUMN_WIDTHS = [5, 15, 10]
ROW_HEIGHT = 2

# Renders the leaderboard
class LeaderboardView(AbstractPageView):
    def __init__(self, root, players, on_home):
        super().__init__(root, Views.LEADERBOARD, len(COLUMN_WIDTHS), on_home)
        self.players = players
        self.closed = tk.Variable()

    def display(self):
        main_frame = tk.Frame(self.root, bg='white')
        self.main_frame = main_frame
        self.main_frame.pack(expand=True, fill=tk.BOTH)
        self.add_title()
        self.add_column_labels()

        for col in range(0, len(COLUMNS)):
            main_frame.columnconfigure(col, weight=1)
            
        for row, player in enumerate(self.players):
            grid_row = row+2
            main_frame.rowconfigure(grid_row, weight=1)
            for col in range(3):
                column_values = [str(row+1), player[0], str(player[1])]
                frame = tk.Frame(main_frame, padx=5, pady=5,relief=tk.RAISED, borderwidth=1, bg='white')
                frame.grid(row=grid_row, column=col, sticky=STICKY)
                tile = tk.Label(frame, borderwidth=1, width=COLUMN_WIDTHS[col], height=ROW_HEIGHT, text=column_values[col],bg="white", fg="black")
                tile.pack(ipadx=1, ipady=1, expand=True)
        self.add_navigator(len(self.players)+2)

    def add_column_labels(self):
        self.main_frame.rowconfigure(1, weight=1)
        for index, column in enumerate(COLUMNS):
            frame = tk.Frame(self.main_frame, relief=tk.RAISED, borderwidth=1, bg='gray')
            frame.grid(row=1, column=index, sticky=STICKY)
            tile = tk.Label(frame, borderwidth=1, width=COLUMN_WIDTHS[0], height=ROW_HEIGHT, text=column,bg="gray")
            tile.pack(expand=True)

    def add_title(self):
        self.main_frame.rowconfigure(0, weight=1, minsize=30)
        super().add_title(frame=self.main_frame, use_grid=True)

    def close(self):
        super().close()
        self.root.geometry("")
        self.on_home()