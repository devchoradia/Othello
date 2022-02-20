from model.player import PLAYER_SYMBOL
import tkinter as tk
from abc import ABC, abstractmethod

# Not implementing this yet
class BoardView(ABC):
    def __init__(self, board):
        self.board = board

    def display(self):
        root = tk.Tk()
        board_size = len(self.board)
        for row in range(board_size):
            for col in range(board_size):
                frame = tk.Frame(relief=tk.RAISED, borderwidth=1, bg='red')
                frame.grid(row=row, column=col)
                label = tk.Label(frame,text='    ',bg='red')
                label.pack()
        root.mainloop()