import tkinter as tk
from view.abstract_page_view import AbstractPageView, ROW_HEIGHT
from model.views import Views, VIEW_TITLES
from model.game_mode import GameMode
from enum import Enum

class Options(Enum):
    LOCAL_GAME = 1
    AI_GAME = 2
    LEADERBOARD = 3
    SETTINGS = 4

OptionLabels = {
    Options.AI_GAME: "Player a computer",
    Options.LOCAL_GAME: "Player locally",
    Options.LEADERBOARD: VIEW_TITLES[Views.LEADERBOARD],
    Options.SETTINGS: VIEW_TITLES[Views.SETTINGS]
}

OptionViews = {
    Options.LOCAL_GAME: Views.GAME,
    Options.AI_GAME: Views.GAME,
    Options.LEADERBOARD: Views.LEADERBOARD,
    Options.SETTINGS: Views.SETTINGS
}

OptionGameModes = {
    Options.LOCAL_GAME: GameMode.LOCAL,
    Options.AI_GAME: GameMode.AI
}


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
        for idx, option in enumerate(Options):
            padyt = 10 if idx != 0 else 20
            button = tk.Button(frame, text=OptionLabels[option], borderwidth=1, width=20, height=ROW_HEIGHT, command=lambda opt=option: self.on_click(opt))
            button.pack(padx=5, pady=(padyt, 5))

    def on_click(self, option):
        super().close()
        view = OptionViews[option]
        if view == Views.GAME:
            self.on_select_page(view, game_mode=OptionGameModes[option])
        else:
            self.on_select_page(view)

    def close(self):
        super().close()

