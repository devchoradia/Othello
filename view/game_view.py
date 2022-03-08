from view.abstract_page_view import AbstractPageView, STICKY
from model.player import PLAYER_COLOR
from model.views import Views
from view.board_view import BoardView
import tkinter as tk

class GameView(AbstractPageView):
    def __init__(self, root, board, board_color, on_home):
        super().__init__(root, Views.GAME, len(board), on_home)
        self.board = board
        self.board_view = BoardView(board, root, board_color)
        self.board_color = board_color

    def display(self):
        self.display_board()
        self.add_navigator(len(self.board)+1, bg=self.board_color)

    def display_current_player(self, player):
        label = tk.Label(relief=tk.RAISED, borderwidth=1, width=5, height=2, font=("Arial", 25), text=f"Player move: {PLAYER_COLOR[player]}",bg=self.board_color, fg="black")
        label.grid(row=len(self.board), columnspan=len(self.board), sticky=STICKY)
        self.widgets.append(label)

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
        label = tk.Label(relief=tk.RAISED, borderwidth=1, width=5, height=2, font=("Arial", 25), text=result_string,bg=self.board_color, fg="black")
        label.grid(row=len(self.board), columnspan=len(self.board), sticky= STICKY)
        self.widgets.append(label)
    
    def close(self):
        self.board_view.destroy_widgets()
        self.destroy_widgets()
        self.on_home()

