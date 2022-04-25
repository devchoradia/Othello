from model.player.player import PLAYER_COLOR
import tkinter as tk
from view.abstract_page_view import GridPageView, STICKY, ROW_HEIGHT, APP_COLOR
from model.game_mode import REMOTE_GAME_REQUEST_STATUS
import threading
from model.views import Views, VIEW_TITLES
from model.session import Session
import time

COLUMNS = ["Player", "Rating", "Request game"]
COLUMN_WIDTHS = [15, 10, 10]
ROW_HEIGHT = 1
PLAY_BUTTON_FONT = ('Tahoma', 14)
MINIMUM_ROWS = 6

# Renders the leaderboard
class OnlinePlayersView(GridPageView):
    def __init__(self, master, players, on_home, request_game):
        super().__init__(master, Views.ONLINE_PLAYERS, on_home=on_home, columnspan=len(COLUMN_WIDTHS), bg='white')
        self.players = players
        self.request_game = request_game
        self.buttons = {}

    def display(self):
        self.add_title()
        self.add_column_labels()
        navigator_row = len(self.players)+2
        for col in range(0, len(COLUMNS)):
            self.columnconfigure(col, weight=1)
            
        for row, player in enumerate(self.players):
            grid_row = row+2
            self.rowconfigure(grid_row, weight=1)
            for col in range(2):
                column_values = [player[0], str(player[1])] # username, rating
                frame = tk.Frame(self, padx=5, pady=5,relief=tk.RAISED, borderwidth=1, bg='white')
                frame.grid(row=grid_row, column=col, sticky=STICKY)
                tile = tk.Label(frame, borderwidth=1, width=COLUMN_WIDTHS[col], height=ROW_HEIGHT, text=column_values[col],bg="white", fg="black")
                tile.pack(ipadx=1, ipady=1, expand=True)
            # Add play button
            command = lambda p=player[0]: self.on_click_play(p)
            clickable = tk.NORMAL
            if player[0] == Session().get_username():
                command = None
                clickable = tk.DISABLED
            frame = tk.Frame(self, padx=5, pady=5,relief=tk.RAISED, borderwidth=1, bg='white')
            frame.grid(row=grid_row, column=2, sticky=STICKY)
            tile = tk.Button(frame, font=PLAY_BUTTON_FONT, text="Play", borderwidth=2, height=ROW_HEIGHT, command=command, state=clickable, bg="white", fg="black", highlightbackground="white")
            self.buttons[player[0]] = tile
            tile.pack(ipadx=1, ipady=1, expand=True)
        
        if len(self.players) < MINIMUM_ROWS:
            navigator_row += MINIMUM_ROWS - len(self.players)
            for row in range(len(self.players), MINIMUM_ROWS):
                grid_row = row + 2
                self.rowconfigure(grid_row, weight=1)
                frame = tk.Frame(self, padx=5, pady=5,relief=tk.RAISED, borderwidth=0, bg=APP_COLOR)
                frame.grid(row=grid_row, columnspan=len(COLUMNS), sticky=STICKY)
        if len(self.players) == 1:
            self.add_no_online_players_message()
        self.add_navigator(navigator_row)
        self.pack(expand=True, fill=tk.BOTH)

    def on_click_play(self, username):
        self.buttons[username].config(state=tk.DISABLED)
        self.buttons[username].config(text=REMOTE_GAME_REQUEST_STATUS.PENDING.value)
        self.request_game(username)

    def update_request(self, username, status):
        self.buttons[username].config(text=status.value)

    def add_no_online_players_message(self):
        grid_row = 2 + len(self.players)
        self.rowconfigure(grid_row, weight=1)
        frame = tk.Frame(self, padx=5, pady=5,relief=tk.RAISED, borderwidth=0, bg=APP_COLOR)
        frame.grid(row=grid_row, columnspan=len(COLUMNS), sticky=STICKY)
        tile = tk.Label(frame, borderwidth=0, height=ROW_HEIGHT, text="No other online players available",bg=APP_COLOR, fg="black")
        tile.pack(ipadx=1, ipady=1, expand=True)

    def add_column_labels(self):
        self.rowconfigure(1, weight=1)
        for index, column in enumerate(COLUMNS):
            frame = tk.Frame(self, relief=tk.RAISED, borderwidth=1, bg='gray')
            frame.grid(row=1, column=index, sticky=STICKY)
            tile = tk.Label(frame, borderwidth=1, width=COLUMN_WIDTHS[0], height=ROW_HEIGHT, text=column,bg="gray")
            tile.pack(expand=True)
