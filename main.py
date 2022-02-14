from model.game import Game
from view.board_console_view import BoardConsoleView
from view.game_console_view import GameConsoleView
from controller.game_controller import GameController

game = Game(board_size = 8)

board_view = BoardConsoleView(game.board)
game_view = GameConsoleView(board_view)

controller = GameController(game, game_view)
controller.run_game()