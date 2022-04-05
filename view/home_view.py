import tkinter as tk
from view.abstract_page_view import PageView, ROW_HEIGHT, BUTTON_FONT, APP_COLOR
from model.views import Views, VIEW_TITLES
from enum import Enum

ROWS = [Views.GAME, Views.LEADERBOARD, Views.SETTINGS]

# Renders the home page
class HomeView(PageView):
    def __init__(self, on_select_page, master):
        super().__init__(master, Views.HOME)
        self.on_select_page = on_select_page
        self['background'] = APP_COLOR
        self['borderwidth'] = 1
        self.configure(background="white")

    def display(self):
        self.add_title()   
        for idx, view in enumerate(ROWS):
            padyt = 10 if idx != 0 else 60
            button = tk.Button(self, text=VIEW_TITLES[view], font=BUTTON_FONT, borderwidth=1, width=20, height=ROW_HEIGHT, command=lambda v=view: self.on_click(v))
            button.pack(padx=5, pady=(padyt, 5))
        self.pack(fill=tk.BOTH, ipadx=50, ipady=50)

    def on_click(self, view):
        self.on_select_page(view)

