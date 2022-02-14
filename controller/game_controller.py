from model.game import Game
from view.game_view import GameView

class GameController:
    def __init__(self, model: Game, view: GameView):
        self.model = model
        self.view = view
    
    def run_game(self):
        game_terminated = False
        while not game_terminated:
            # TODO: check if player has valid turn
            self.view.display_board()
            self.view.display_curr_player(self.model.curr_player)

            row, col = self.view.get_move()
            is_legal = self.model.is_legal_move(row, col)
            while not is_legal:
                self.view.display_illegal_move(row, col)
                row, col = self.view.get_move()
                is_legal = self.model.is_legal_move(row, col)
            
            self.model.make_move(row, col)
            game_terminated = self.model.is_game_terminated()
            if not game_terminated:
                self.model.switch_player_turn()