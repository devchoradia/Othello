from model.game import Game
from model.views import Views
from model.game_mode import GameMode
from view.home_view import HomeView
from view.game_view import GameView
from view.settings_view import SettingsView
from view.leaderboard_view import LeaderboardView
from view.register import Register
from view.login import AccountInfoView
from controller.game_controller import GameController
from server.database_client import DatabaseClient, LOGIN_RESULT, REGISTER_RESULT, REGISTER_RESULT_MESSAGE
from model.player import PLAYER_COLOR
import tkinter as tk

class AppController:
    def __init__(self, database_client: DatabaseClient):
        self.board_size = 4
        self.database_client = database_client
        self.current_view = Views.LOGIN
        self.board_color = PLAYER_COLOR[0]
    
    def init_app(self):
        self.root = tk.Tk()
        self.root['background'] = '#cfbd9b'
        self.root.after(1000, lambda: self.on_select_page(self.current_view))
        self.root.mainloop()

    def start_game(self, game_mode=GameMode.LOCAL):
        game = Game(board_size = self.board_size)
        controller = GameController(game, root=self.root, game_mode=game_mode, on_home=self.on_home, board_color=self.board_color)
        controller.run_game()

    def display_home(self):
        home = HomeView(on_select_page=self.on_select_page, root=self.root)
        home.display()

    def display_login(self):
        login = AccountInfoView(self.root, self.on_login, lambda: self.on_select_page(Views.REGISTER), on_home=self.on_home)
        login.display()

    def display_register(self):
        register = AccountInfoView(self.root, self.on_register, lambda: self.on_select_page(Views.LOGIN), self.on_home, view=Views.REGISTER, \
            submit_results=REGISTER_RESULT, result_messages=REGISTER_RESULT_MESSAGE, submit_label="REGISTER", switch_view_label="Log in")
        register.display()

    def on_select_page(self, view, game_mode=None):
        self.current_view = view
        if view == Views.LOGIN:
            self.display_login()
        elif view == Views.GAME:
            self.start_game(game_mode)
        elif view == Views.SETTINGS:
            self.display_settings()
        elif view == Views.LEADERBOARD:
            self.display_leaderboard()
        elif view == Views.REGISTER:
            self.display_register()
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

    def on_login(self, username, password):
        result, (username, rating) = self.database_client.login(username, password)
        if result == LOGIN_RESULT.SUCCESS:
            self.username = username
            self.rating = rating
        return result

    def on_register(self, username, password):
        result, (username, rating) = self.database_client.register_user(username, password)
        if result == LOGIN_RESULT.SUCCESS:
            self.username = username
            self.rating = rating
        return result

    def on_win(self):
        pass
        
