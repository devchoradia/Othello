from model.game import Game
from view.board_console_view import BoardConsoleView
from view.board_view import BoardView
from view.game_console_view import GameConsoleView
from view.game_view import GameView
from controller.game_controller import GameController

game = Game(board_size = 4)

#board_view = BoardConsoleView(game.board)
#game_view = GameConsoleView(board_view)
board_view = BoardView(game.board)
game_view = GameView(board_view)
controller = GameController(game, game_view)
controller.run_game()