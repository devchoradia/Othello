from enum import IntEnum

class Player(IntEnum):
    X = 1
    0 = 2

PLAYER_SYMBOL = {
    Player.X: 'X',
    Player.0: 'O'
}