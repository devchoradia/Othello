from model.game import Game
from view.game_view import GameView

class GameController:
    def __init__(self, model: Game, view: GameView):
        self.model = model
        self.view = view
    
    def run_game(self):
        game_terminated = False
        while not game_terminated:
            self.view.display_board()
            self.view.display_curr_player(self.model.curr_player)

            row, col = self.view.get_move()
            # check legality
            # while not legal, display illegal move and re-get move

            # make move in model
            # check game termination / switch player turn