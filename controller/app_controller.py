from model.game import Game
from model.views import Views
from view.home_view import HomeView
from view.game_view import GameView
from view.settings_view import SettingsView
from view.leaderboard_view import LeaderboardView
from view.register import Register
from view.login import AccountInfoView
from controller.game_controller import GameController
from server.database_client import DatabaseClient, LOGIN_RESULT, REGISTER_RESULT, REGISTER_RESULT_MESSAGE
from model.player.player import Player
from model.player.AIPlayer import AIPlayer
from model.player.LocalPlayer import LocalPlayer
from model.player.RemotePlayer import RemotePlayer
from model.settings import Settings, Setting
from model.game_mode import GameMode
from model.ai.minimax_ai import MinimaxAI
from model.observer import Observer
from model.session import Session
from client.client import Client
from server.server import Request
import tkinter as tk

class AppController(Observer):
    def __init__(self):
        super().__init__([])
        self.client = Client()
        self.client.set_observer(self)
        self.game_state = (None, None, None)
        self.remote_game_state = (None, None, None)

    def init_app(self):
        self.root = tk.Tk()
        self.root.after(1000, lambda: self.display_login())
        self.root.mainloop()

    def start_game(self):
        game = Game(board_size = Settings().get_board_size())
        player_color = Player.BLACK
        # Resume previous game if it was interrupted
        if Session().is_logged_in() and Settings().get_game_mode() == GameMode.REMOTE:
            opponent, board_size, player_color = self.remote_game_state
            if opponent is None:
                self.request_opponent()
                return
            game = Game(board_size=board_size)
        elif Session().is_logged_in():
            board, game_mode, current_player = self.game_state
            if all(item is not None for item in (board, game_mode, current_player)) and Settings().get_board_size() == len(board) and game_mode == Settings().get_game_mode():
                game = Game(board_size=len(board), game=game, curr_player=current_player)
        self.current_view.destroy()
        self.game = game
        game.add_observer(self)
        view = GameView(master=self.root, board=game.board, on_home=self.on_home, board_color = Settings().get_board_color())
        self.current_view = view
        view.display()
        game_mode = Settings().get_game_mode()
        players = [LocalPlayer(view)]
        if game_mode == GameMode.LOCAL:
            players.append(LocalPlayer(view, player_color=Player.WHITE))
        elif game_mode == GameMode.AI:
            players.append(AIPlayer(ai=MinimaxAI(), view=view))
        elif game_mode == GameMode.REMOTE:
            local_player = LocalPlayer(view, player_color=player_color)
            remote_player = RemotePlayer(player_color=Player(len(Player) + 1 - player_color), game=game, local_player=local_player, client=self.client)
            players = [local_player, remote_player]
            players.sort(key=lambda p: p.player_color)
        else:
            raise ValueError("Received invalid game mode: " + str(game_mode))
        controller = GameController(game, view, players=players)
        controller.run_game()

    def request_opponent(self):
        self.current_view.display_awaiting_component()
        self.client.request_opponent(Session().get_username(), Settings().get_board_size())

    def display_home(self):
        self.current_view = HomeView(on_select_page=self.on_select_page, master=self.root)
        self.current_view.display()

    def display_login(self):
        self.current_view = AccountInfoView(self.root, self.on_login, lambda: self.on_select_page(Views.REGISTER), on_home=self.on_home)
        self.current_view.display()

    def display_register(self):
        self.current_view = AccountInfoView(self.root, self.on_register, lambda: self.on_select_page(Views.LOGIN), self.on_home, view=Views.REGISTER, \
            submit_results=REGISTER_RESULT, result_messages=REGISTER_RESULT_MESSAGE, submit_label="REGISTER", switch_view_label="Log in")
        self.current_view.display()

    def on_select_page(self, view):
        if view == Views.LOGIN:
            self.current_view.destroy()
            self.display_login()
        elif view == Views.GAME:
            self.start_game()
        elif view == Views.SETTINGS:
            self.current_view.destroy()
            self.display_settings()
        elif view == Views.LEADERBOARD:
            self.current_view.destroy()
            self.request_leaderboard()
        elif view == Views.REGISTER:
            self.current_view.destroy()
            self.display_register()
        else:
            self.current_view.destroy()
            self.display_home()

    def request_leaderboard(self):
        self.client.get_leaderboard()
        
    def display_leaderboard(self, players):
        self.current_view = LeaderboardView(self.root, players=players, on_home=self.on_home)
        self.current_view.display()
    
    def display_settings(self):
        self.current_view = SettingsView(master=self.root, on_home=self.on_home)
        self.current_view.display()

    def on_home(self):
        self.on_select_page(Views.HOME)

    def on_login(self, username, password):
        self.client.login(username, password)

    def update_settings(self, message_body):
        board_size, board_color, game_mode = message_body
        new_state = {
            Setting.BOARD_SIZE: board_size,
            Setting.BOARD_COLOR: board_color,
            Setting.GAME_MODE: game_mode
        }
        Settings().update_settings(new_state)

    def handle_message(self, message):
        message_type = message.message_type
        body = message.body
        if message_type == Request.LOGIN or message_type == Request.REGISTER:
            result, (username, rating) = body
            self.login_result(result, username, rating)
        elif message_type in [Request.GET_GAME_STATE, Request.REMOVE_GAME_STATE, Request.UPDATE_GAME_STATE]:
            self.game_state = body
        elif message_type == Request.LEADERBOARD:
            self.display_leaderboard(body)
        elif message_type == Request.GET_SETTINGS:
            self.update_settings(body)
        elif message_type == Request.REMOTE_PLAY:
            self.remote_game_state = body
            self.start_game()
    
    def login_result(self, result, username, rating):
        print("loggin int")
        print(result)
        if result == LOGIN_RESULT.SUCCESS:
            print("logged in")
            Session().log_in(username, rating)
            self.client.get_game_state(username)
            self.client.get_settings(username)
        elif result == REGISTER_RESULT.SUCCESS:
            print("registered")
            Session().log_in(username, rating)
        self.current_view.login_result(result)

    def on_register(self, username, password):
        self.client.register(username, password)

    def update(self, subject, message=None):
        if subject == self.client:
            self.handle_message(message)
        # Don't save game state if user is playing remotely
        elif not Session().is_logged_in() or Settings().get_game_mode() == GameMode.REMOTE:
            print("logged in")
            return
        elif subject == self.game and self.game.is_game_terminated():
            self.client.remove_game_state(Session().get_username())
            if Settings().get_game_mode() == GameMode.REMOTE:
                self.client.end_remote_game(Session().get_username())
                self.remote_game_state = (None, None, None)
        elif subject == self.game:
            print("updating game state")
            self.client.update_game_state(subject.board, Settings().get_game_mode(), subject.curr_player, Session().get_username())

    def on_win(self):
        pass
        
