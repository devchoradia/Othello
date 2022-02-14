from model.player import PLAYER_SYMBOL

TILE_WIDTH = 4
EMPTY_TILE = ' ' * TILE_WIDTH
EMPTY_SPACE = ' ' * (TILE_WIDTH - 1)

class BoardConsoleView:
    def __init__(self, board):
        self.board = board

    def display(self):
        column_labels = EMPTY_TILE + ' ' + EMPTY_SPACE.join(list(map(lambda x: str(x), range(1, len(self.board) + 1)))) + '  '
        border = EMPTY_SPACE + ("-" * (len(self.board) * TILE_WIDTH + 1))
        ascii_representation = []
        for index, row in enumerate(self.board):
            ascii_characters = map(lambda x: PLAYER_SYMBOL[x], row)
            ascii_characters_list = list(ascii_characters)
            tiles_characters = ' | '.join(ascii_characters_list)
            ascii_representation.append(' ' + str(index + 1) + ' ' + '| ' + tiles_characters + ' |')
            ascii_representation.append(border)
        text_display = '\n'.join(ascii_representation)
        print(column_labels)
        print(border)
        print(text_display)
