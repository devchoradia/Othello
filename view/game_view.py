from abc import ABC, abstractmethod
from model.player import PLAYER_COLOR
from view.board_view import BoardView
import tkinter as tk

# Not implementing this yet
class GameView(ABC):
    def __init__(self, board):
        self.root = tk.Tk()
        self.board = board
        self.board_view = BoardView(board, self.root)

    def mainloop(self):
        self.root.mainloop()

    def display_login(self):
        pass

    def add_board(self):
        self.board_view.display()

    def display_board(self, current_player = None):
        self.add_board()
        if current_player is not None:
            self.add_current_player(current_player)
        self.root.update()

    def display_illegal_move(self, row, col):
        self.board_view.display(illegal_move=(row, col))
        self.root.update()

    def get_move(self):
        return self.board_view.get_move()

    def add_current_player(self, player):
        label = tk.Label(relief=tk.RAISED, borderwidth=1, width=5, height=2, font=("Arial", 25), text=f"Player move: {PLAYER_COLOR[player]}",bg="green", fg="black")
        label.grid(row=len(self.board), columnspan=len(self.board), sticky= tk.W+tk.E+tk.N+tk.S)

    def display_winner(self, player):
        result_string = f"{PLAYER_COLOR[player].upper()} WINS"
        if player == 0:
            result_string = "DRAW"
        self.add_board()
        label = tk.Label(relief=tk.RAISED, borderwidth=1, width=5, height=2, font=("Arial", 25), text=result_string,bg="green", fg="black")
        label.grid(row=len(self.board), columnspan=len(self.board), sticky= tk.W+tk.E+tk.N+tk.S)
    
    def close_game(self):
        self.root.destroy()

