from model.player import PLAYER_COLOR
import tkinter as tk
from abc import ABC, abstractmethod

# Renders the board
class BoardView(ABC):
    def __init__(self, board):
        self.board = board

    def display(self):
        root = tk.Tk()
        board_size = len(self.board)
        for row in range(board_size):
            root.rowconfigure(row+1)
            root.columnconfigure(row+1)
            for col in range(board_size):
                player = self.board[row][col]
                tile_color = PLAYER_COLOR[player]
                relief = None if player == 0 else tk.RAISED
                frame = tk.Frame(relief=tk.RAISED, borderwidth=1, bg='green')
                frame.grid(row=row, column=col,padx=0, pady=0, ipadx=0, ipady=0)
                label = tk.Label(frame, relief=relief, borderwidth=1, width=5, height=3, text='    ',bg=tile_color)
                label.pack(padx=5, pady=5, expand=True)
        root.mainloop()