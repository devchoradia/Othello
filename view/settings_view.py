from tkinter import ttk
import tkinter as tk
from abc import ABC, abstractmethod
from model.player import PLAYER_COLOR


class SettingsView(ABC):
    def __init__(self, on_close, update_color, update_size, color=PLAYER_COLOR[0], size=4):
        self.root = tk.Tk()
        self.on_close = on_close
        self.update_color = update_color
        self.update_size = update_size
        self.board_color = tk.StringVar()
        self.board_color.set(color)
        self.board_size = tk.IntVar()
        self.board_size.set(size)
        self.saved = tk.BooleanVar()
        self.saved.set(False)

    def display(self):
        self.root.geometry("800x400")

        # label widget
        l1 = tk.Label(self.root, text="Board Size:")
        l2 = tk.Label(self.root, text="Board Color:")

        # grid
        l1.grid(row=0, column=0, sticky=tk.W, pady=2)
        l2.grid(row=1, column=0, sticky=tk.W, pady=2)

        # Create an instance of Menu in the frame
        board_color_menu = ttk.OptionMenu(self.root, self.board_color, "green", "blue", "orange", "yellow", "purple", "pink")
        board_color_menu.grid(row=1, column=1)

        # entry widgets, used to take entry from user
        board_size_menu = ttk.OptionMenu(self.root, self.board_size, 4, 6, 8, 10, 12)

        # this will arrange entry widgets
        board_size_menu.grid(row=0, column=1, pady=2)

        # Save button
        save = tk.Button(self.root, text="Save", command=lambda: self.save())
        save.grid(row=2, columnspan=2, padx=2, pady=2)
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.root.mainloop()

    def save(self):
        self.saved.set(True)
        self.close()

    def close(self):
        self.root.destroy()
        if(self.saved.get()):
            self.update_color(self.board_color.get())
            self.update_size(self.board_size.get())
        self.on_close()
