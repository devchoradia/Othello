from abc import ABC, abstractmethod
import tkinter as tk
from model.views import Views, VIEW_TITLES

STICKY = tk.W+tk.E+tk.N+tk.S
ROW_HEIGHT = 2
BUTTON_FONT = ("Palatino", 30)
HOME_BUTTON_FONT = ("Palatino", 20)
TEXT_FONT = ('Tahoma', 16)
APP_COLOR = '#cfbd9b'

class AbstractPageView(tk.Frame):
    '''
    Abstract class for a page view
    '''
    def __init__(self, master, page_view, on_home=None, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.title = VIEW_TITLES[page_view]
        self.on_home = on_home
        master.title(self.title)

    @abstractmethod
    def display(self):
        '''
        Display the page view
        '''
        pass

    @abstractmethod
    def add_title(self):
        '''
        Adds the title of the page to the view and the window 
        '''         

    @abstractmethod
    def add_navigator(self, row):
        '''
        Adds the navigator (home button) to the bottom of the page
        '''

class PageView(AbstractPageView):
    def __init__(self, master, page_view, on_home=None, **kwargs):
        super().__init__(master, page_view, on_home=on_home, **kwargs)

    def add_title(self):
        title_frame = tk.Frame(self, bg=APP_COLOR)
        title_frame.pack(fill=tk.X)
        label = tk.Label(title_frame, bg=APP_COLOR, relief=tk.RAISED, borderwidth=1, height=ROW_HEIGHT, font=("Palatino", 40), text=self.title, fg="black")
        label.pack(expand=True, fill=tk.BOTH)    

    def add_navigator(self):
        frame = tk.Frame(self, borderwidth=1, bg=APP_COLOR, highlightbackground = 'black', highlightcolor='black', highlightthickness=1)
        frame.pack(expand=True, fill=tk.BOTH)
        home_button = tk.Button(frame, text=VIEW_TITLES[Views.HOME], borderwidth=1, height=ROW_HEIGHT, \
            command=self.on_home, bg=APP_COLOR, highlightbackground=APP_COLOR)
        home_button.pack(pady=10)

class GridPageView(AbstractPageView):
    def __init__(self, master, page_view, columnspan, on_home=None, **kwargs):
        super().__init__(master, page_view, on_home=on_home, **kwargs)
        self.columnspan = columnspan

    def add_title(self):
        self.rowconfigure(0, weight=1, minsize=30)
        label = tk.Label(self, relief=tk.RAISED, bg=APP_COLOR, borderwidth=1, height=ROW_HEIGHT, font=("Palatino", 40), text=self.title ,fg="black")
        label.grid(row=0, columnspan=self.columnspan, sticky=STICKY)

    def add_navigator(self, row):
        home_frame = tk.Frame(self, bg=APP_COLOR, borderwidth=1)
        home_frame.grid(row=row, columnspan=self.columnspan, sticky=STICKY)
        home_button = tk.Button(home_frame, font=HOME_BUTTON_FONT, text=VIEW_TITLES[Views.HOME], borderwidth=2, height=ROW_HEIGHT, \
        command=self.on_home, bg=APP_COLOR, highlightbackground=APP_COLOR)
        home_button.pack(expand=True, fill=tk.Y, pady=10)

