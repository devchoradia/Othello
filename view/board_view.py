from model.player import PLAYER_COLOR
import tkinter as tk
import threading
import time
from view.abstract_page_view import STICKY

ILLEGAL_MOVE_COLOR = "red"

# Renders the board
class BoardView:
    def __init__(self, board, root, board_color=PLAYER_COLOR[0]):
        self.board = board
        self.root = root
        self.move_clicked = tk.Variable()
        self.board_color = board_color
        self.widgets = []
        self.illegal_move = None

    def display(self):
        self.illegal_move = None
        board_size = len(self.board)
        self.destroy_widgets()
        self.widgets = []
        for row in range(board_size):
            widgets = []
            for col in range(board_size):
                frame = self.add_tile(row, col)
                widgets.append(frame)
            self.widgets.append(widgets)

    def add_tile(self, row, col, is_illegal=False):
        player = self.board[row][col]
        tile_color = self.get_tile_color(player, is_illegal)
        frame_color = ILLEGAL_MOVE_COLOR if is_illegal else self.board_color
        tile_relief = tk.RAISED
        pad_x = 5
        ipad_x = 0
        if player == 0:
            pad_x = 0
            ipad_x = 5
            tile_relief = None
        tile_relief = None if player == 0 else tk.RAISED
        pad_x = 0 if player == 0 else 5
        ipad_x = 5 if player == 0 else 0
        frame = tk.Frame(relief=tk.RAISED, borderwidth=1, bg=frame_color)
        frame.grid(row=row, column=col,padx=0, pady=0, ipadx=0, ipady=0, sticky=STICKY)
        tile = tk.Label(frame, relief=tile_relief, borderwidth=1, width=5, height=3, text='    ',bg=tile_color)
        tile.bind("<Button-1>", lambda x, r=row, c=col: self.on_click_tile(row=r, col=c))
        tile.pack(padx=pad_x, ipadx=ipad_x, pady=pad_x, ipady=ipad_x, expand=True)
        return frame

    def display_illegal_move(self, row, col):
        self.widgets[row][col].destroy()
        frame = self.add_tile(row, col, is_illegal=True)
        self.widgets[row][col] = frame
        if self.illegal_move is not None:
            old_row, old_col = self.illegal_move
            self.widgets[old_row][old_col].destroy()
            frame = self.add_tile(old_row, old_col)
            self.widgets[old_row][old_col] = frame
        self.illegal_move = (row, col)

    def on_click_tile(self, row, col):
        self.move_clicked.set((row, col))
    
    def show_legal_moves(self, valid_moves):
        self.display(self, valid_moves)

    def get_move(self):
        self.move_clicked = tk.Variable()
        initial_value = self.move_clicked.get()
        self.widgets[0][0].wait_variable(self.move_clicked)
        return self.move_clicked.get()
    
    def get_tile_color(self, player, is_illegal):
        if player != 0:
            return PLAYER_COLOR[player]
        return ILLEGAL_MOVE_COLOR if is_illegal else self.board_color

    def destroy_widgets(self):
        for row in self.widgets:
            for widget in row:
                widget.destroy()