from model.game import Game
from view.game_view import GameView
from model.ai.minimax_ai import MinimaxAI
from model.game_mode import GameMode
from model.player import Player, AI_PLAYER, HUMAN_PLAYER
import time

class GameController:
    def __init__(self, model: Game, view: GameView, game_mode: GameMode = GameMode.LOCAL):
        self.model = model
        self.view = view
        self.game_mode = game_mode

    # Run the game
    def run_game(self):
        game_terminated = False
        self.view.display()
        # Continue requesting and performing players' movements until the game is over
        while not game_terminated:
            # If the current player has no valid move, switch turns and move on
            if not self.model.has_valid_move():
                self.model.switch_player_turn()
                continue
            # Display the board and current player
            self.view.display_board()
            self.view.display_current_player(self.model.curr_player)
            # Get the next move
            row, col = self.get_move()
            # Check legality of move
            is_legal = self.model.is_legal_move(row, col)
            # If illegal move, display it and re-request a move
            while not is_legal:
                self.view.display_illegal_move(row, col)
                row, col = self.view.get_move()
                is_legal = self.model.is_legal_move(row, col)
            
            # Once the move is legal, update the board
            self.model.make_move(row, col)

            # End the loop if the game is over as a result. Otherwise, switch turns
            game_terminated = self.model.is_game_terminated()
            if not game_terminated:
                self.model.switch_player_turn()
        # Display the final state of the board and the winner
        self.view.display_board()
        self.view.display_winner(self.model.get_winner())

    # Get the move from the current player
    def get_move(self):
        if self.game_mode == GameMode.AI and self.model.curr_player == AI_PLAYER:  
            return MinimaxAI().decision(self.model.board)
        else:
            return self.view.get_move()
