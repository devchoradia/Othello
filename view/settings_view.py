import tkinter as tk
from abc import ABC, abstractmethod
from model.player import PLAYER_COLOR

COLUMNS = ["Setting", "Value"]
COLUMN_WIDTHS = [7, 7]
ROW_HEIGHT = 2
STICKY = tk.W+tk.E+tk.N+tk.S
SETTINGS = ["Board Size", "Board color"]
SETTING_OPTIONS = [[4, 6, 8, 10], ["green", "blue", "cyan", "yellow", "magenta"]]

class SettingsView(ABC):
    def __init__(self, root, update_color, update_size, on_home, color=PLAYER_COLOR[0], size=4):
        self.root = root
        self.update_color = update_color
        self.update_size = update_size
        self.on_home = on_home
        self.board_color = tk.StringVar()
        self.board_color.set(color)
        self.board_size = tk.IntVar()
        self.board_size.set(size)
        self.saved = tk.BooleanVar()
        self.saved.set(False)
        self.widgets = []

    def display(self):
        self.add_title(0) # row 0
        self.add_column_labels(1) # row 1
        self.add_settings(2) # beginning at row 2
        self.add_save(4) # row 4
        self.add_navigator(5) # row 5

    def add_settings(self, start_row):
        initial_values = [self.board_size, self.board_color]
        for index, setting in enumerate(SETTINGS):
            row = start_row + index
            # Setting name
            label_frame = tk.Frame(padx=5, pady=5,relief=tk.RAISED, borderwidth=1, bg='white')
            label_frame.grid(row=row, column=0, sticky=STICKY)
            tile = tk.Label(label_frame, borderwidth=1, width=COLUMN_WIDTHS[0], height=ROW_HEIGHT, text=setting,bg="white", fg="black")
            tile.pack(ipadx=1, ipady=1, expand=True)
            # Setting value
            options_frame = tk.Frame(padx=5, pady=5,relief=tk.RAISED, borderwidth=1, bg='white')
            options_frame.grid(row=row, column=1, sticky=STICKY)
            option = tk.OptionMenu(options_frame, initial_values[index], *SETTING_OPTIONS[index])
            option.config(bg="white", fg="black")
            option.pack(ipadx=1, ipady=1, expand=True)
            # Add widgets
            self.widgets.extend([label_frame, options_frame])

    def add_save(self, row):
        frame = tk.Frame(padx=5, pady=5,relief=tk.RAISED, borderwidth=1, bg='white')
        frame.grid(row=row, columnspan=len(COLUMNS), sticky=STICKY)
        save = tk.Button(frame, text="Save", command=self.save, background="white", bg="white", highlightbackground="white")
        save.pack()
        self.widgets.append(frame)

    def add_navigator(self, row):
        home_button = tk.Button(self.root, text="Home", borderwidth=1, height=ROW_HEIGHT, \
            command=self.close, bg="white", highlightbackground="white")
        home_button.grid(row=row, columnspan=len(COLUMNS), sticky=STICKY)
        self.widgets.append(home_button)
    
    def add_title(self, row):
        label = tk.Label(relief=tk.RAISED, borderwidth=1, width=20, height=ROW_HEIGHT, font=("Arial", 25), text="Settings",bg="white", fg="black")
        label.grid(row=row, columnspan=len(COLUMNS), sticky= tk.W+tk.E+tk.N+tk.S)
        self.widgets.append(label)

    def add_column_labels(self, row):
        for index, column in enumerate(COLUMNS):
            frame = tk.Frame(relief=tk.RAISED, borderwidth=1, bg='gray')
            frame.grid(row=row, column=index, sticky= tk.W+tk.E+tk.N+tk.S)
            tile = tk.Label(frame, borderwidth=1, width=COLUMN_WIDTHS[0], height=ROW_HEIGHT, text=column,bg="gray")
            tile.pack(expand=True)
            self.widgets.append(frame)

    def save(self):
        self.saved.set(True)
        self.close()

    def close(self):
        self.destroy_widgets()
        if(self.saved.get()):
            self.update_color(self.board_color.get())
            self.update_size(self.board_size.get())
        self.on_home()

    def destroy_widgets(self):
        for widget in self.widgets:
            widget.destroy()
