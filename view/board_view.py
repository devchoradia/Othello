from model.player.player import PLAYER_COLOR
import tkinter as tk
import threading
import time
from view.abstract_page_view import STICKY

ILLEGAL_MOVE_COLOR = "red"
ROW_KEY = "tile"
MIN_TILE_LENGTH = 50

# Renders the board
class BoardView(tk.Frame):
    def __init__(self, board, master, board_color=PLAYER_COLOR[0]):
        super().__init__(master, bg="white", width=500, height=500, background="white")
        self.master = master
        self.board = board
        self.board_color = board_color
        self.widgets = []
        self.illegal_move = None
        self.requested_move = tk.Variable()
        self.move_handler = None
        self.illegal_move = None
        self.content_frame = tk.Frame(self)
        board_size = len(self.board)
        for row in range(board_size):
            widgets = []
            self.content_frame.rowconfigure(row, weight=1, uniform=ROW_KEY)
            self.content_frame.columnconfigure(row, weight=1, uniform=ROW_KEY)
            for col in range(board_size):
                frame_tile = self.add_tile(row, col)
                widgets.append(frame_tile)
            self.widgets.append(widgets)
        self.enforce_aspect_ratio()
        self.pack(expand=True, fill=tk.BOTH, pady=(0,50))

    def enforce_aspect_ratio(self):
        content_frame = self.content_frame
        def enforce_aspect_ratio(event):
            aspect_ratio = 1.0
            desired_width = event.width
            desired_height = int(event.width / aspect_ratio)
            if desired_height > event.height:
                desired_height = event.height
                desired_width = int(event.height * aspect_ratio)
            content_frame.place(in_=self, relx=0.5, rely=0.5, anchor=tk.CENTER, 
                width=desired_width, height=desired_height)
        self.bind("<Configure>", enforce_aspect_ratio)

    def update_board(self):
        for row in range(len(self.board)):
            for col in range(len(self.board)):
                frame, tile = self.widgets[row][col]
                player = self.board[row][col]
                if self.get_tile_color(player) != tile.cget('bg') or (row, col) == self.illegal_move:
                    frame.destroy()
                    frame, tile = self.add_tile(row, col)
                    self.widgets[row][col] = (frame, tile)

    
    def set_move_handler(self, move_handler):
        self.move_handler = move_handler

    def remove_move_handler(self):
        self.move_handler = None

    def add_tile(self, row, col):
        player = self.board[row][col]
        tile_color = self.get_tile_color(player)

        # Create tile frame
        frame = tk.Frame(self.content_frame, relief=tk.RAISED, borderwidth=2, bg=self.board_color)
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
        return frame, tile

    def on_click_move(self, row, col):
        '''
        Whenever a click is moved, we notify the observers
        '''
        if self.move_handler != None:
            self.requested_move.set((row, col))
            self.move_handler()

    def get_requested_move(self):
        return self.requested_move.get()

    def get_tile_in_frame(self, frame):
        children_widgets = frame.winfo_children()
        for child_widget in children_widgets:
            if child_widget.winfo_class() == 'Label':
                return child_widget
        print("Couldn't find child of board tile frame")

    def display_illegal_move(self, row, col):
        frame, tile = self.widgets[row][col]
        frame.config(bg=ILLEGAL_MOVE_COLOR)
        bg = tile.cget("bg")
        if bg == self.board_color:
            tile.config(bg=ILLEGAL_MOVE_COLOR)
        if self.illegal_move is not None:
            old_row, old_col = self.illegal_move
            old_frame, old_tile = self.widgets[old_row][old_col]
            old_frame.config(bg=self.board_color)
            if old_tile.cget("bg") == ILLEGAL_MOVE_COLOR:
                old_tile.config(bg=self.board_color)
        self.illegal_move = (row, col)
    
    def show_legal_moves(self, valid_moves):
        self.display(self, valid_moves)
    
    def get_tile_color(self, player):
        if player != 0:
            return PLAYER_COLOR[player]
        return self.board_color
