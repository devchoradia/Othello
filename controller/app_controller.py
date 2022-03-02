from model.game import Game
from model.views import Views
from view.home_view import HomeView
from view.game_view import GameView
from view.settings_view import SettingsView
from view.leaderboard_view import LeaderboardView
from controller.game_controller import GameController
from server.database_client import DatabaseClient

class AppController:
    def __init__(self, database_client: DatabaseClient):
        self.board_size = 4
        self.database_client = database_client
        self.current_view = Views.HOME#Views.LOGIN
    
    def init_app(self):
        self.on_select_page(self.current_view)

    def start_game(self):
        game = Game(board_size = self.board_size)
        game_view = GameView(game.board, on_close=self.on_close)
        controller = GameController(game, game_view)
        controller.start_game()

    def display_home(self):
        home = HomeView(on_select_page=self.on_select_page)
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
        leaderboard = LeaderboardView(players, on_close=self.on_close)
        leaderboard.display()
    
    def display_settings(self):
        settings = SettingsView(on_select_page=self.on_select_page)
        settings.display()

    def on_close(self):
        if self.current_view != Views.LOGIN:
            self.on_select_page(Views.HOME)

    def on_win(self):
        pass
        
