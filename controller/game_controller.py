from model.game import Game
from view.game_view import GameView
from model.ai.minimax_ai import MinimaxAI
from model.settings import GameMode
from model.player.player import Player, GamePlayer
from model.observer import Observer

class GameController(Observer):
    def __init__(self, model: Game, view: GameView, players: [GamePlayer]):
        super().__init__([*players, model]) # Subscribe to the model and players
        self.model = model
        self.view = view
        self.players = {players[i].player_color: players[i] for i in range(0, len(players))}

    # Run the game
    def run_game(self):
        self.view.display_current_player(self.model.curr_player)
        self.players[self.model.curr_player].request_move()

    # Observer is notified of an update from the view or model
    def update(self, subject):
        # If the subject is a player, get the move and handle it
        if subject in list(self.players.values()):
            row, col = subject.get_requested_move()
            self.request_move(row, col, subject)
        # If the subject is the model, update the view of the game
        if subject == self.model:
            self.update_view()

    # Event handler when player clicks a move
    def request_move(self, row, col, player):
        print("requested move")
        # Ignore if it's not the player's move
        if player.player_color != self.model.curr_player:
            return
        # Check legality of move
        is_legal = self.model.is_legal_move(row, col)
        # If illegal move, display it and wait again
        if not is_legal:
            self.view.display_illegal_move(row, col)
            player.request_move()
        # Make the move
        else:
            self.make_move(row, col)
       
    def make_move(self, row, col):
        # Make the move
        self.model.make_move(row, col)
        # End game if the game is over as a result. Otherwise, switch turns
        game_terminated = self.model.is_game_terminated()
        # Switch player turns
        self.model.switch_player_turn()
        if not game_terminated:
            # If the other player has no turn, switch back
            if not self.model.has_valid_move():
                self.model.switch_player_turn()
            # Request the move from the current player
            self.players[self.model.curr_player].request_move()
        else:
            self.end_game()

    # Displays the game using the GameView
    def update_view(self):
        self.view.display_board()
        if self.model.is_game_terminated():
            self.view.display_winner(self.model.get_winner())
        else:
            self.view.display_current_player(self.model.curr_player)

    def end_game(self):
        print("game controller ended")
        # Display the final state of the board and the winner
        self.view.display_board()
        self.view.display_winner(self.model.get_winner())
