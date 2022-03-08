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

    def display(self):
        frame = tk.Frame(self.root)
        frame.configure(background="white")
        self.add_title(frame=frame)
        for row, column in enumerate(ROWS):
            button = tk.Button(frame, text=VIEW_TITLES[column], borderwidth=1, width=40, height=ROW_HEIGHT, command=lambda col=column: self.on_click(col))
            button.pack(padx=5, pady=5)
        frame.pack()
        self.widgets.append(frame)

    def on_click(self, view):
        self.destroy_widgets()
        self.on_select_page(view)

    def close(self):
        self.destroy_widgets()

