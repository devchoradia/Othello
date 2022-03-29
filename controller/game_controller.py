from model.game import Game
from view.game_view import GameView
from model.ai.minimax_ai import MinimaxAI
from model.settings import GameMode
from model.player import Player, AI_PLAYER, HUMAN_PLAYER
import time
from model.observer import Observer

class GameController(Observer):
    def __init__(self, model: Game, view, game_mode: GameMode = GameMode.LOCAL):
        super().__init__([view.board_view, model])
        self.model = model
        self.game_mode = game_mode
        self.view = view
        game_terminated = False

    # Run the game
    def run_game(self):
        self.view.display()
        self.view.display_current_player(self.model.curr_player)

    # Get the move from the ai
    def ai_move(self):
        row, col = MinimaxAI().decision(self.model.board)
        self.make_move(row, col)

    # Observer is notified of an update from the view or model
    def update(self, subject):
        if subject == self.view.board_view:
            row, col = self.view.board_view.get_requested_move()
            self.click_move(row, col)
        if subject == self.model:
            self.update_view()

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
            # Switch player turns
            self.model.switch_player_turn()
            # If the other player has no turn, switch back
            if not self.model.has_valid_move():
                self.model.switch_player_turn()

            # If other player is AI, get that move
            if self.game_mode == GameMode.AI and self.model.curr_player == AI_PLAYER:
                self.view.root.after(1000, self.ai_move)

    # Displays the game using the GameView
    def update_view(self):
        self.view.display_board()
        if self.model.is_game_terminated():
            self.view.display_winner(self.model.get_winner())
        else:
            self.view.display_current_player(self.model.curr_player)

    def end_game(self):
        # Display the final state of the board and the winner
        self.view.display_board()
        self.view.display_winner(self.model.get_winner())
