from enum import IntEnum

class Player(IntEnum):
    BLACK = 1
    WHITE = 2

PLAYER_SYMBOL = {
    Player.BLACK: 'X',
    Player.WHITE: 'O',
    0: ' '
}

PLAYER_COLOR = {
    Player.BLACK: 'black',
    Player.WHITE: 'white',
    0: 'green'
}

AI_PLAYER = Player.WHITE
HUMAN_PLAYER = Player.BLACK