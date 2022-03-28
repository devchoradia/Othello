from model.player import PLAYER_COLOR
import tkinter as tk
import threading
import time
from view.abstract_page_view import STICKY

ILLEGAL_MOVE_COLOR = "red"
ROW_KEY = "tile"
MIN_TILE_LENGTH = 50

# Renders the board
class BoardView:
    def __init__(self, board, root, on_click_move, board_color=PLAYER_COLOR[0]):
        self.board = board
        self.root = root
        self.board_color = board_color
        self.widgets = []
        self.illegal_move = None
        self.on_click_move = on_click_move

    def display(self):
        self.illegal_move = None
        board_size = len(self.board)
        self.clear_frame()
        self.widgets = []
        for row in range(board_size):
            widgets = []
            self.root.rowconfigure(row, weight=1, uniform=ROW_KEY, minsize=MIN_TILE_LENGTH)
            self.root.columnconfigure(row, weight=1, uniform=ROW_KEY, minsize=MIN_TILE_LENGTH)
            for col in range(board_size):
                frame = self.add_tile(row, col)
                widgets.append(frame)
            self.widgets.append(widgets)

    def add_tile(self, row, col, is_illegal=False):
        player = self.board[row][col]
        tile_color = self.get_tile_color(player, is_illegal)

        # Create tile frame
        frame_color = ILLEGAL_MOVE_COLOR if is_illegal else self.board_color
        frame = tk.Frame(self.root, relief=tk.RAISED, borderwidth=2, bg=frame_color)
        frame.grid(row=row, column=col,padx=0, pady=0, ipadx=0, ipady=0, sticky=STICKY)

        # Add tile
        tile_relief = tk.RAISED
        pad_x = 10
        ipad_x = 0
        if player == 0:
            ipad_x = pad_x
            pad_x = 0
            tile_relief = None

        tile = tk.Label(frame, relief=tile_relief, borderwidth=1, text='    ',bg=tile_color)
        tile.bind("<Button-1>", lambda x, r=row, c=col: self.on_click_move(r, c))
        tile.pack(padx=pad_x, ipadx=ipad_x, pady=pad_x, ipady=ipad_x, expand=True, fill=tk.BOTH)
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
    
    def show_legal_moves(self, valid_moves):
        self.display(self, valid_moves)
    
    def get_tile_color(self, player, is_illegal):
        if player != 0:
            return PLAYER_COLOR[player]
        return ILLEGAL_MOVE_COLOR if is_illegal else self.board_color

    def clear_frame(self):
        widgets = self.root.winfo_children()
        for widget in widgets:
            widget.destroy()