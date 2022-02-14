from model.player import PLAYER_SYMBOL

# Not implementing this yet
class BoardView(ABC):
    def __init__(self, board):
        self.board = board

    def display_board(self):
        ascii_representation = []
        for row in board:
            ascii_characters = map(lambda x: PLAYER_SYMBOL[x], row)
            ascii_characters_list = list(ascii_characters)
            ascii_representation.append(''.join(ascii_characters_list))
        return '\n'.join(ascii_representation)