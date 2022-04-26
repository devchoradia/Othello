import tkinter as tk

from model.session import Session
from model.views import Views, VIEW_TITLES
from view.abstract_page_view import PageView, ROW_HEIGHT, BUTTON_FONT, APP_COLOR

ROWS = [Views.GAME, Views.LEADERBOARD, Views.SETTINGS, Views.LOGIN]


# Renders the home page
class HomeView(PageView):
    def __init__(self, on_select_page, master, rating=None):
        super().__init__(master, Views.HOME)
        self.on_select_page = on_select_page
        self['background'] = APP_COLOR
        self['borderwidth'] = 1
        self.configure(background="white")
        self.loading_label = None
        self.rating_label = None

    def display(self):
        self.add_title()
        self.add_rating()
        for idx, view in enumerate(ROWS):
            button = tk.Button(self, text=self.get_button_label(view), font=BUTTON_FONT, borderwidth=1, width=20,
                               height=ROW_HEIGHT, command=lambda v=view: self.on_click(v))
            button.pack(padx=5, pady=(10, 5))
        self.add_loading_label()
        self.pack(fill=tk.BOTH, ipadx=50, ipady=50)

    def add_loading_label(self):
        frame = tk.Frame(self, bg="white")
        frame.pack(expand=True, fill=tk.BOTH)
        l = tk.Label(frame, text="", bg='white', fg='red', font='Helvetica 15')
        l.pack(pady=10)
        self.loading_label = l

    def add_rating(self):
        font, size = BUTTON_FONT
        rating_font = (font, size, "bold")
        frame = tk.Frame(self, bg="white")
        frame.pack()
        rating = Session().get_ELORating()
        text = ""
        if rating is not None:
            text = f"Rating: {str(rating)}"
        rating = tk.Label(frame, text=text, bg='white', fg='black', font=rating_font)
        rating.pack(pady=(50, 10))
        self.rating_label = rating

    def update_rating(self):
        rating = Session().get_ELORating()
        text = ""
        if rating is not None:
            text = f"Rating: {str(rating)}"
        self.rating_label.config(text=text)

    def display_awaiting_component(self):
        if self.loading_label is not None:
            self.loading_label.config(text="Looking for opponent...")

    def display_opponent_disconnected(self, message):
        if self.loading_label is not None:
            self.loading_label.config(text=message)

    def get_button_label(self, view):
        if view == Views.GAME:
            return "Start game"
        if view == Views.LOGIN and Session().is_logged_in():
            return "Log out"
        return VIEW_TITLES[view]

    def on_click(self, view):
        self.on_select_page(view)
