import tkinter as tk

from model.session import Session
from model.views import Views
from view.abstract_page_view import GridPageView, STICKY, ROW_HEIGHT, TEXT_FONT

COLUMNS = ["Rank", "Player", "Rating"]
COLUMN_WIDTHS = [5, 15, 10]
ROW_HEIGHT = 2
CURRENT_USER_FONT = ('Tahoma', 16, 'bold')


# Renders the leaderboard
class LeaderboardView(GridPageView):
    def __init__(self, master, players, on_home):
        super().__init__(master, Views.LEADERBOARD, on_home=on_home, columnspan=len(COLUMN_WIDTHS), bg='white')
        self.players = players

    def display(self):
        self.add_title()
        self.add_column_labels()
        for col in range(0, len(COLUMNS)):
            self.columnconfigure(col, weight=1)

        for row, player in enumerate(self.players):
            grid_row = row + 2
            self.rowconfigure(grid_row, weight=1)
            for col in range(3):
                column_values = [str(row + 1), player[0], str(player[1])]
                frame = tk.Frame(self, padx=5, pady=5, relief=tk.RAISED, borderwidth=1, bg='white')
                frame.grid(row=grid_row, column=col, sticky=STICKY)
                font = CURRENT_USER_FONT if player[0] == Session().get_username() else TEXT_FONT
                tile = tk.Label(frame, borderwidth=1, width=COLUMN_WIDTHS[col], height=ROW_HEIGHT, font=font,
                                text=column_values[col], bg="white", fg="black")
                tile.pack(ipadx=1, ipady=1, expand=True)
        self.add_navigator(len(self.players) + 2)
        self.pack(expand=True, fill=tk.BOTH)

    def add_column_labels(self):
        self.rowconfigure(1, weight=1)
        for index, column in enumerate(COLUMNS):
            frame = tk.Frame(self, relief=tk.RAISED, borderwidth=1, bg='gray')
            frame.grid(row=1, column=index, sticky=STICKY)
            tile = tk.Label(frame, borderwidth=1, width=COLUMN_WIDTHS[0], height=ROW_HEIGHT, text=column, bg="gray")
            tile.pack(expand=True)
