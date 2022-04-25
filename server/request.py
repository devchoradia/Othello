from enum import Enum

class Request(Enum):
    LOGIN = "login"
    LOGOUT = "logout"
    REGISTER = "register"
    REMOVE_GAME_STATE = "remove game state"
    UPDATE_GAME_STATE = "update game state"
    GET_GAME_STATE = "get game state"
    LEADERBOARD = "leaderboard"
    UPDATE_SETTINGS = "update settings"
    GET_SETTINGS = "get settings"
    UPDATE_REMOTE_GAME = "update remote game"
    GET_ONLINE_PLAYERS = "get online players"
    END_REMOTE_GAME = "end remote game"
    OPPONENT_DISCONNECTED = "opponent disconnected"
    UPDATE_ELO_RATING = "update ELO rating"
    REQUEST_REMOTE_GAME = "request remote game"
    UPDATE_REMOTE_GAME_STATUS = "update remote game status"

class Message:
    def __init__(self, message_type: Request, body):
        self.message_type = message_type
        self.body = body