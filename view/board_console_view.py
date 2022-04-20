from model.player.player import PLAYER_SYMBOL

TILE_WIDTH = 4
EMPTY_TILE = ' ' * TILE_WIDTH
EMPTY_SPACE = ' ' * (TILE_WIDTH - 1)

class BoardConsoleView:
    def __init__(self, board):
        self.board = board

    # Renders the board in the console
    def display(self):
        # Label the column numbers
        column_labels = EMPTY_TILE + ' ' + EMPTY_SPACE.join(list(map(lambda x: str(x), range(1, len(self.board) + 1)))) + '  '
        # Board border
        border = EMPTY_SPACE + ("-" * (len(self.board) * TILE_WIDTH + 1))
        # String representation of tiles; each string renders one row
        ascii_representation = []
        for index, row in enumerate(self.board):
            # Convert players to string characters
            ascii_characters = map(lambda x: PLAYER_SYMBOL[x], row)
            ascii_characters_list = list(ascii_characters)
            # Add borders/spacing between tiles
            tiles_characters = ' | '.join(ascii_characters_list)
            # Add row labels
            ascii_representation.append(' ' + str(index + 1) + ' ' + '| ' + tiles_characters + ' |')
            # Add row border
            ascii_representation.append(border)
        # Combine rows into one string
        text_display = '\n'.join(ascii_representation)
