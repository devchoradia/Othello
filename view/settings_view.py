# Import module
from tkinter import *
from tkinter.ttk import *
# object
from tkinter import ttk

import tkinter as tk
from abc import ABC, abstractmethod


class SettingsView(ABC):
    def __init__(self, on_select_page):
        self.root = tk.Tk()
        self.on_select_page = on_select_page
        self.closed = tk.Variable()

    def display(self):
        self.root.geometry("800x400")

        # label widget
        l1 = Label(self.root, text="Board Size:")
        l2 = Label(self.root, text="Tile Color:")

        # grid
        l1.grid(row=0, column=0, sticky=W, pady=2)
        l2.grid(row=1, column=0, sticky=W, pady=2)

        # Access the Menu Widget using StringVar function
        clicked = StringVar()
        # initial text
        clicked.set("Black")
        # Create an instance of Menu in the frame
        main_menu = OptionMenu(self.root, clicked, "Black", "White", "Red", "Green", "Blue", "Yellow", "Purple")
        main_menu.grid(row=2, column=0)

        # entry widgets, used to take entry from user
        e1 = Entry(self.root)

        # this will arrange entry widgets
        e1.grid(row=0, column=1, pady=2)

        self.root.mainloop()
