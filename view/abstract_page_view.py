from abc import ABC, abstractmethod
import tkinter as tk

STICKY = tk.W+tk.E+tk.N+tk.S
ROW_HEIGHT = 2

class AbstractPageView(ABC):
    '''
    Abstract class for a page view
    '''
    def __init__(self, root, title, columnspan, on_home):
        self.root = root
        self.widgets = []
        self.title = title
        self.columnspan = columnspan
        self.on_home = on_home

    @abstractmethod
    def display(self):
        pass

    @abstractmethod
    def close(self):
        pass

    def destroy_widgets(self):
        for widget in self.widgets:
            widget.destroy()

    def add_title(self, row=0, frame=None):
        label = tk.Label(relief=tk.RAISED, borderwidth=1, width=20, height=ROW_HEIGHT, font=("Arial", 25), text=self.title ,bg="white", fg="black")
        if frame is not None:
            label = tk.Label(frame, relief=tk.RAISED, borderwidth=1, width=40, height=ROW_HEIGHT, font=("Arial", 25), text="Home",bg="white", fg="black")
            label.pack(expand=True)
        else:
            label.grid(row=row, columnspan=self.columnspan, sticky=STICKY)
        self.widgets.append(label)

    def add_navigator(self, row, bg="white"):
        home_button = tk.Button(self.root, text="Home", borderwidth=1, height=ROW_HEIGHT, \
            command=self.close, bg=bg, highlightbackground="white")
        if self.columnspan is None:
            home_button.pack(expand=True)
        else:
            home_button.grid(row=row, columnspan=self.columnspan, sticky=STICKY)
        self.widgets.append(home_button)
