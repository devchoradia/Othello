from enum import Enum

class Request(Enum):
    LOGIN = "login"
    REGISTER = "register"
    REMOVE_GAME_STATE = "remove game state"
    UPDATE_GAME_STATE = "update game state"
    GET_GAME_STATE = "get game state"
    LEADERBOARD = "leaderboard"
    UPDATE_SETTINGS = "update settings"
    GET_SETTINGS = "get settings"
    REMOTE_PLAY = "remote play"
    UPDATE_REMOTE_GAME = "update remote game"
    END_REMOTE_GAME = "end remote game"
    OPPONENT_DISCONNECTED = "opponent disconnected"

class Message:
    def __init__(self, message_type: Request, body):
        self.message_type = message_type
        self.body = body