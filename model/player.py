from enum import IntEnum

class Player(IntEnum):
    X = 1
    O = 2

PLAYER_SYMBOL = {
    Player.X: 'X',
    Player.O: 'O',
    0: ' '
}
