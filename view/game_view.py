from abc import ABC, abstractmethod
from model.player import PLAYER_SYMBOL

# Not implementing this yet
class GameView(ABC):
    def __init__(self, board_view):
        self.board_view = board_view

    def mainloop(self):
        self.board_view.mainloop()

    def display_login(self):
        pass

    def display_board(self):
        self.board_view.display()

    def display_illegal_move(self, row, col):
        print("Illegal move: ", row, col)

    def get_move(self):
        return self.board_view.get_move()

    def display_curr_player(self, player):
        print("Current player: " + PLAYER_SYMBOL[player])

    def display_winner(self, player):
        print("Game over.")
        if player == 0:
            print("Draw.")
        else:
            print("Player " + PLAYER_SYMBOL[player] + " won.")

# abstract methods: $abstract_method
# get_move, #display_player, display_illegal_moves