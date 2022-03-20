import tkinter as tk
from view.abstract_page_view import AbstractPageView, ROW_HEIGHT
from model.views import Views, VIEW_TITLES

ROWS = [Views.GAME, Views.LEADERBOARD, Views.SETTINGS]

# Renders the home page
class HomeView(AbstractPageView):
    def __init__(self, on_select_page, root):
        super().__init__(root, Views.HOME, None, None)
        self.on_select_page = on_select_page
        self.closed = tk.Variable()
        self.root['background'] = 'white'

    def display(self):
        frame = tk.Frame(self.root)
        frame.configure(background="white")
        frame.pack(fill=tk.BOTH, ipadx=50, ipady=50)
        self.add_title(frame=frame)
        for row, column in enumerate(ROWS):
            padyt = 10 if row != 0 else 20
            button = tk.Button(frame, text=VIEW_TITLES[column], borderwidth=1, width=20, height=ROW_HEIGHT, command=lambda col=column: self.on_click(col))
            button.pack(padx=5, pady=(padyt, 5))

    def on_click(self, view):
        super().close()
        self.on_select_page(view)

    def close(self):
        super().close()

