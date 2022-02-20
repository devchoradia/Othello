from model.player import PLAYER_COLOR
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
            root.rowconfigure(row+1)#, weight=1)
            root.columnconfigure(row+1)#, weight=1)
            for col in range(board_size):
                frame = tk.Frame(relief=tk.RAISED, borderwidth=1, bg='green')
                frame.grid(row=row, column=col,padx=0, pady=0, ipadx=0, ipady=0)
                print(frame.grid_info())
                label = tk.Label(frame, width=5, height=3, text='    ',bg='green')
                label.pack(padx=0, pady=0, expand=True)
        root.mainloop()