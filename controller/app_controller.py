from model.game import Game
from model.views import Views
from view.home_view import HomeView
from view.game_view import GameView
from view.settings_view import SettingsView
from view.leaderboard_view import LeaderboardView
from controller.game_controller import GameController
from server.database_client import DatabaseClient
from model.player import PLAYER_COLOR
import tkinter as tk

class AppController:
    def __init__(self, database_client: DatabaseClient):
        self.board_size = 4
        self.database_client = database_client
        self.current_view = Views.HOME#Views.LOGIN
        self.board_color = PLAYER_COLOR[0]
    
    def init_app(self):
        self.root = tk.Tk()
        self.root.after(1000, lambda: self.on_select_page(self.current_view))
        self.root.mainloop()

    def start_game(self):
        game = Game(board_size = self.board_size)
        game_view = GameView(root=self.root, board=game.board, on_home=self.on_home, board_color = self.board_color)
        controller = GameController(game, game_view)
        controller.run_game()

    def display_home(self):
        home = HomeView(on_select_page=self.on_select_page, root=self.root)
        home.display()

    def on_select_page(self, view):
        self.current_view = view
        if view == Views.LOGIN:
            self.display_login()
        elif view == Views.GAME:
            self.start_game()
        elif view == Views.SETTINGS:
            self.display_settings()
        elif view == Views.LEADERBOARD:
            self.display_leaderboard()
        else:
            self.display_home()
        
    def display_leaderboard(self):
        players = self.database_client.get_leaderboard()
        leaderboard = LeaderboardView(root=self.root, players=players, on_home=self.on_home)
        leaderboard.display()
    
    def display_settings(self):
        settings = SettingsView(root=self.root, update_color=self.on_change_board_color, \
            update_size=self.on_change_board_size, color=self.board_color, size=self.board_size, on_home=self.on_home)
        settings.display()

    def on_change_board_size(self, size):
        self.board_size = size

    def on_change_board_color(self, color):
        self.board_color = color

    def on_home(self):
        self.on_select_page(Views.HOME)

    def on_win(self):
        pass
        
