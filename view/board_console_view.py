from model.player import PLAYER_SYMBOL

TILE_WIDTH = 4

class BoardConsoleView:
    def __init__(self, board):
        self.board = board

    def display(self):
        border = "-" * (len(self.board) * TILE_WIDTH + 1)
        ascii_representation = []
        for row in self.board:
            ascii_characters = map(lambda x: PLAYER_SYMBOL[x], row)
            ascii_characters_list = list(ascii_characters)
            tiles_characters = ' | '.join(ascii_characters_list)
            ascii_representation.append('| ' + tiles_characters + ' |')
        text_display = '\n'.join(ascii_representation)
        print(border)
        print(text_display)
        print(border)
