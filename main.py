from model.game import Game
from view.board_console_view import BoardConsoleView
from view.board_view import BoardView
from view.game_console_view import GameConsoleView
from view.game_view import GameView
from controller.game_controller import GameController

game = Game(board_size = 8)

game_view = GameView(game.board)
controller = GameController(game, game_view)
controller.start_game()