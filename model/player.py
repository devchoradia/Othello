from enum import IntEnum

class Player(IntEnum):
    BLACK = 1
    WHITE = 2

PLAYER_SYMBOL = {
    Player.BLACK: 'X',
    Player.WHITE: 'O',
    0: ' '
}
