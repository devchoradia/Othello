from abc import ABC, abstractmethod
from model.player import PLAYER_COLOR
from view.board_view import BoardView
import tkinter as tk

class GameView(ABC):
    def __init__(self, root, board, board_color, on_home):
        self.root = root
        self.board = board
        self.board_view = BoardView(board, root, board_color)
        self.board_color = board_color
        self.on_home = on_home
        self.widgets = []

    def add_board(self):
        self.board_view.display()

    def display_board(self, current_player = None):
        self.add_navigator()
        self.add_board()
        if current_player is not None:
            self.add_current_player(current_player)
        self.root.update()

    def add_navigator(self):
        home_button = tk.Button(self.root, text="Home", borderwidth=1, height=2, bg=self.board_color, fg="black", \
            command=self.close_game)
        home_button.grid(row=len(self.board) + 1, columnspan=len(self.board), sticky= tk.W+tk.E+tk.N+tk.S)
        self.widgets.append(home_button)

    def display_illegal_move(self, row, col):
        self.board_view.display(illegal_move=(row, col))
        self.root.update()

    def get_move(self):
        return self.board_view.get_move()

    def add_current_player(self, player):
        label = tk.Label(relief=tk.RAISED, borderwidth=1, width=5, height=2, font=("Arial", 25), text=f"Player move: {PLAYER_COLOR[player]}",bg=self.board_color, fg="black")
        label.grid(row=len(self.board), columnspan=len(self.board), sticky= tk.W+tk.E+tk.N+tk.S)
        self.widgets.append(label)

    def display_winner(self, player):
        self.add_navigator()
        result_string = f"{PLAYER_COLOR[player].upper()} WINS"
        if player == 0:
            result_string = "DRAW"
        self.add_board()
        label = tk.Label(relief=tk.RAISED, borderwidth=1, width=5, height=2, font=("Arial", 25), text=result_string,bg=self.board_color, fg="black")
        label.grid(row=len(self.board), columnspan=len(self.board), sticky= tk.W+tk.E+tk.N+tk.S)
        self.widgets.append(label)
    
    def close_game(self):
        for widget in self.widgets + self.board_view.widgets:
            widget.destroy()
        self.on_home()

