from model.player import PLAYER_COLOR
import tkinter as tk
from abc import ABC, abstractmethod
import threading
import time

# Renders the board
class BoardView(ABC):
    def __init__(self, board):
        self.board = board
        self.root = tk.Tk()
        self.move_clicked = tk.Variable()
        self.tiles = []

    def mainloop(self):
         self.root.mainloop()

    def display(self, valid_moves = None):
        board_size = len(self.board)
        all_moves_clickable = valid_moves == None
        if all_moves_clickable:
            valid_moves = []
        i = 0
        for row in range(board_size):
            self.root.rowconfigure(row+1)
            self.root.columnconfigure(row+1)
            for col in range(board_size):
                player = self.board[row][col]
                is_valid_move = all_moves_clickable or (row, col) in valid_moves
                tile_color = PLAYER_COLOR[player]
                disabled = not all_moves_clickable and (row, col) not in valid_moves
                button_state = tk.NORMAL if disabled else tk.ACTIVE
                tile_relief = None if player == 0 else tk.RAISED
                pad_x = 0 if player == 0 else 5
                ipad_x = 5 if player == 0 else 0
                frame = tk.Frame(relief=tk.RAISED, borderwidth=1, bg='green')
                frame.grid(row=row, column=col,padx=0, pady=0, ipadx=0, ipady=0, sticky= tk.W+tk.E+tk.N+tk.S)
                tile = tk.Label(frame, relief=tile_relief, borderwidth=1, width=5, height=3, text='    ',bg=tile_color)
                tile.bind("<Button-1>", lambda x, r=row, c=col, clickable=is_valid_move: self.on_click_tile(row=r, col=c, is_valid_move=clickable))
                tile.pack(padx=pad_x, ipadx=ipad_x, pady=pad_x, ipady=ipad_x, expand=True)
                self.tiles.append(tile)
                i += 1
        self.root.update()

    def on_click_tile(self, row, col, is_valid_move=True):
        if is_valid_move:
            self.move_clicked.set((row, col))
    
    def show_legal_moves(self, valid_moves):
        self.display(self, valid_moves)

    def get_move(self):
        self.move_clicked = tk.Variable()
        initial_value = self.move_clicked.get()
        self.tiles[0].wait_variable(self.move_clicked)
        return self.move_clicked.get()