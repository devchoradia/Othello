from model.game import Game
import copy

'''
Facade Design Pattern

Simplifies the Game interface, hiding the implementation of the model from the user (e.g. minimax ai).
This class allows users to work with the board without having to worry about the persistent
details of the model class.
'''
class GameStateManager:
    @staticmethod
    def make_move(board, player, row, col):
        model = GameStateManager.create_model(board, player)
        model.make_move(row, col)
        return model.board

    @staticmethod
    def get_valid_moves(board, player):
        return GameStateManager.create_model(board, player).get_valid_moves(player)

    @staticmethod
    def has_valid_move(board, player):
        return GameStateManager.create_model(board, player).has_valid_move(player)
        
    @staticmethod
    def create_model(board, curr_player):
        return Game(board_size=len(board), board=copy.deepcopy(board), curr_player=curr_player)

    
    