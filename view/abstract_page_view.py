from abc import ABC, abstractmethod
import tkinter as tk
from model.views import Views, VIEW_TITLES

STICKY = tk.W+tk.E+tk.N+tk.S
ROW_HEIGHT = 2

class AbstractPageView(ABC):
    '''
    Abstract class for a page view
    '''
    def __init__(self, root, page_view, columnspan=None, on_home=None):
        self.root = root
        self.title = VIEW_TITLES[page_view]
        self.columnspan = columnspan
        self.on_home = on_home

    @abstractmethod
    def display(self):
        '''
        Display the page view
        '''
        pass

    @abstractmethod
    def close(self):
        '''
        Destroy widgets and close the page
        '''
        pass

    def destroy_widgets(self):
        '''
        Destroy all widgets in the page
        '''
        widgets = self.root.winfo_children()
        for widget in widgets:
            widget.destroy()

    def add_title(self, row=0, frame=None):
        '''
        Adds the title of the page to the view and the window 
        '''
        self.root.title(self.title)
        label = tk.Label(relief=tk.RAISED, borderwidth=1, width=20, height=ROW_HEIGHT, font=("Arial", 25), text=self.title ,bg="white", fg="black")
        if frame is not None:
            label = tk.Label(frame, relief=tk.RAISED, borderwidth=1, width=40, height=ROW_HEIGHT, font=("Arial", 25), text="Home",bg="white", fg="black")
            label.pack(expand=True)
        else:
            label.grid(row=row, columnspan=self.columnspan, sticky=STICKY)

    def add_navigator(self, row, bg="white"):
        home_button = tk.Button(self.root, text=VIEW_TITLES[Views.HOME], borderwidth=1, height=ROW_HEIGHT, \
            command=self.close, bg=bg, highlightbackground="white")
        if self.columnspan is None:
            home_button.pack(expand=True)
        else:
            home_button.grid(row=row, columnspan=self.columnspan, sticky=STICKY)
