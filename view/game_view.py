from view.abstract_page_view import AbstractPageView, STICKY
from model.player.player import PLAYER_COLOR
from model.views import Views
from view.board_view import BoardView, ROW_KEY, MIN_TILE_LENGTH
import tkinter as tk

class GameView(AbstractPageView):
    def __init__(self, root, board, board_color, on_home):
        super().__init__(root, Views.GAME, columnspan=len(board), on_home=on_home)
        self.board = board
        self.root.geometry(f'{MIN_TILE_LENGTH*len(board)}x{MIN_TILE_LENGTH*(len(board)+2)}')
        self.root.aspect(len(board), len(board)+2, len(board), len(board)+2)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.board_view = BoardView(board, root, board_color)
        self.board_color = board_color

    def display(self):
        self.display_board()
        self.add_navigator()

    def display_current_player(self, player):
        self.root.rowconfigure(len(self.board), weight=1, uniform=ROW_KEY,  minsize=MIN_TILE_LENGTH)
        label = tk.Label(relief=tk.RAISED, borderwidth=2, font=("Arial", 16), text=f"Player move: {PLAYER_COLOR[player]}",bg=self.board_color, fg="black")
        label.grid(row=len(self.board), columnspan=len(self.board), sticky=STICKY)
        self.add_navigator()

    def display_board(self):
        self.board_view.display()

    def display_illegal_move(self, row, col):
        self.board_view.display_illegal_move(row, col)

    def get_move(self):
        return self.board_view.get_move()

    def display_winner(self, player):
        result_string = f"{PLAYER_COLOR[player].upper()} WINS"
        if player == 0:
            result_string = "DRAW"
        label = tk.Label(relief=tk.RAISED, borderwidth=2, width=5, height=2, font=("Arial", 20), text=result_string,bg=self.board_color, fg="black")
        label.grid(row=len(self.board), columnspan=len(self.board), sticky= STICKY)
        self.add_navigator()

    def add_navigator(self):
        self.root.rowconfigure(len(self.board)+1, weight=1, uniform=ROW_KEY, minsize=MIN_TILE_LENGTH)
        super().add_navigator(len(self.board)+1, bg=self.board_color, omit_height=True, use_grid=True, pady=15)
    
    def close(self):
        self.board_view.clear_frame()
        super().close()
        self.root['background'] = 'white'
        self.root.aspect("", "", "", "")
        self.root.geometry("")
        self.on_home()

