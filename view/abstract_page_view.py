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
        widgets = self.root.winfo_children()
        for widget in widgets:
            widget.destroy()

    def add_title(self, row=0, frame=None, use_grid=False):
        '''
        Adds the title of the page to the view and the window 
        '''
        self.root.title(self.title)
        if frame is None:
            frame = self.root
        if use_grid:
            label = tk.Label(frame, relief=tk.RAISED, borderwidth=1, height=ROW_HEIGHT, font=("Arial", 25), text=self.title ,bg="white", fg="black")
            label.grid(row=row, columnspan=self.columnspan, sticky=STICKY)
        else:
            # label = tk.Label(frame, relief=tk.RAISED, borderwidth=1, width=30, height=ROW_HEIGHT, font=("Arial", 25), text="Home",bg="white", fg="black")
            # label.pack(expand=True)
            title_frame = tk.Frame(frame, bg="white")
            title_frame.pack(fill=tk.X)
            # title_frame.place(anchor='n', relx=0.5)
            label = tk.Label(title_frame, relief=tk.RAISED, borderwidth=1, width=frame.cget("width"), height=ROW_HEIGHT, font=("Arial", 25), text=self.title, bg="white", fg="black")
            label.pack(expand=True, fill=tk.BOTH)            

    def add_navigator(self, row, bg="white", frame=None, height=ROW_HEIGHT, omit_height=False, use_grid=False, pady=10):
        '''
        Adds the navigator (home button) to the bottom of the page
        '''
        if frame is None:
            frame = self.root
        if omit_height:
            height = None
        if use_grid:
            home_frame = tk.Frame(frame, bg=bg)
            home_frame.grid(row=row, columnspan=self.columnspan, sticky=STICKY)
            home_button = tk.Button(home_frame, text=VIEW_TITLES[Views.HOME], borderwidth=1, height=height, \
            command=self.close, bg=bg, highlightbackground=bg)
            home_button.pack(expand=True, fill=tk.Y, pady=pady)
        else:
            home_button = tk.Button(frame, text=VIEW_TITLES[Views.HOME], borderwidth=1, height=height, \
            command=self.close, bg=bg, highlightbackground=bg)
            home_button.pack(pady=pady)
            

