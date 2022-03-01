from model.game import Game
from view.board_console_view import BoardConsoleView
from view.board_view import BoardView
from view.game_console_view import GameConsoleView
from view.game_view import GameView
from controller.game_controller import GameController

from view.leaderboard_view import LeaderboardView
from controller.app_controller import AppController
from server.database_client import DatabaseClient

client = DatabaseClient()
app = AppController(client)
app.init_app()