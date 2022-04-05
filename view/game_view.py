from view.abstract_page_view import STICKY, ROW_HEIGHT, PageView, BUTTON_FONT, APP_COLOR
from model.player.player import PLAYER_COLOR, Player
from model.views import Views, VIEW_TITLES
from view.board_view import BoardView, ROW_KEY, MIN_TILE_LENGTH
import tkinter as tk

class GameView(PageView):
    def __init__(self, master, board, board_color, on_home):
        super().__init__(master, Views.GAME, on_home=on_home)
        self['background'] = 'white'
        self.board = board
        self.board_color = board_color
        self.add_title()

    def display(self):
        self.add_current_player()
        self.board_view = BoardView(self.board, self, self.board_color)
        self.add_navigator()
        self.pack(expand=True, fill=tk.BOTH)

    def display_current_player(self, player):
        self.current_player_label.config(text=f"Player move: {PLAYER_COLOR[player]}")

    def display_board(self):
        self.board_view.update_board()

    def display_illegal_move(self, row, col):
        self.board_view.display_illegal_move(row, col)

    def get_move(self):
        return self.board_view.get_move()

    def add_current_player(self, player=Player.BLACK):
        frame = tk.Frame(self, bg="white", borderwidth=1)
        frame.pack(expand=True, fill=tk.BOTH)
        label = tk.Label(frame, borderwidth=2, font=BUTTON_FONT, height=ROW_HEIGHT, text=f"Player move: {PLAYER_COLOR[player]}",bg='white', fg="black")
        label.pack(padx=10, pady=10)
        self.current_player_label = label

    def display_winner(self, player):
        result_string = f"{PLAYER_COLOR[player].upper()} WINS"
        if player == 0:
            result_string = "DRAW"
        self.current_player_label.config(text=result_string)

