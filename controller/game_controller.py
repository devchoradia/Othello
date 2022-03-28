from model.game import Game
from view.game_view import GameView
from model.ai.minimax_ai import MinimaxAI
from model.game_mode import GameMode
from model.player import Player, AI_PLAYER, HUMAN_PLAYER
import time

class GameController:
    def __init__(self, model: Game, on_home, board_color, root, game_mode: GameMode = GameMode.LOCAL):
        self.model = model
        self.game_mode = game_mode
        self.view = GameView(root=root, board=model.board, on_home=on_home, board_color = board_color, on_click_move=self.click_move)
        game_terminated = False

    # Run the game
    def run_game(self):
        self.view.display()
        self.view.display_current_player(self.model.curr_player)

    # Get the move from the ai
    def ai_move(self):
        row, col = MinimaxAI().decision(self.model.board)
        self.make_move(row, col)

    # Event handler when player clicks a move
    def click_move(self, row, col):
        # Ignore if not player's turn
        if self.game_mode == GameMode.AI and self.model.curr_player != HUMAN_PLAYER:
            return
        # Check legality of move
        is_legal = self.model.is_legal_move(row, col)
        # If illegal move, display it and wait again
        if not is_legal:
            self.view.display_illegal_move(row, col)
        # Make the move
        else :
            self.make_move(row, col)
       
    def make_move(self, row, col):
        # Make the move
        self.model.make_move(row, col)
        # End game if the game is over as a result. Otherwise, switch turns
        game_terminated = self.model.is_game_terminated()
        if not game_terminated:
            self.model.switch_player_turn()
        else:
            self.end_game()
            return

        # If the other player has no turn, switch back
        if not self.model.has_valid_move():
            self.model.switch_player_turn()
        
        # Display the board and current player
        self.view.display_board()
        self.view.display_current_player(self.model.curr_player)

        # If other player is AI, get that move
        if self.game_mode == GameMode.AI and self.model.curr_player == AI_PLAYER:
            self.view.root.after(2000, self.ai_move)

    def end_game(self):
        # Display the final state of the board and the winner
        self.view.display_board()
        self.view.display_winner(self.model.get_winner())
