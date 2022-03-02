from model.player import PLAYER_COLOR
import tkinter as tk
from abc import ABC, abstractmethod
import threading
import time

# Renders the board
class BoardView(ABC):
    def __init__(self, board, root=None, board_color=PLAYER_COLOR[0]):
        self.board = board
        self.root = root if root is not None else tk.Tk()
        self.move_clicked = tk.Variable()
        self.tile_buttons = []
        self.board_color = board_color

    def mainloop(self):
         self.root.mainloop()

    def display(self, illegal_move = None):
        board_size = len(self.board)
        for row in range(board_size):
            for col in range(board_size):
                player = self.board[row][col]
                tile_color = self.get_tile_color(player)
                if illegal_move == (row, col):
                    tile_color = "red"
                tile_relief = None if player == 0 else tk.RAISED
                pad_x = 0 if player == 0 else 5
                ipad_x = 5 if player == 0 else 0
                frame = tk.Frame(relief=tk.RAISED, borderwidth=1, bg='green')
                frame.grid(row=row, column=col,padx=0, pady=0, ipadx=0, ipady=0, sticky= tk.W+tk.E+tk.N+tk.S)
                tile = tk.Label(frame, relief=tile_relief, borderwidth=1, width=5, height=3, text='    ',bg=tile_color)
                tile.bind("<Button-1>", lambda x, r=row, c=col: self.on_click_tile(row=r, col=c))
                tile.pack(padx=pad_x, ipadx=ipad_x, pady=pad_x, ipady=ipad_x, expand=True)
                self.tile_buttons.append(tile)

    def on_click_tile(self, row, col):
        self.move_clicked.set((row, col))
    
    def show_legal_moves(self, valid_moves):
        self.display(self, valid_moves)

    def get_move(self):
        self.move_clicked = tk.Variable()
        initial_value = self.move_clicked.get()
        self.tile_buttons[0].wait_variable(self.move_clicked)
        return self.move_clicked.get()
    
    def get_tile_color(self, player):
        return self.board_color if player == 0 else PLAYER_COLOR[player]