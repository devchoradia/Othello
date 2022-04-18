import threading
from model.player.player import PLAYER_COLOR
from enum import IntEnum, Enum
from model.session import Session
from model.game_mode import GameMode
from client.client import Client

class Setting(IntEnum):
    BOARD_SIZE = 0
    BOARD_COLOR = 1
    GAME_MODE = 2

SETTING_LABELS = {
    Setting.BOARD_SIZE: "Board Size",
    Setting.BOARD_COLOR: "Board color",
    Setting.GAME_MODE: "Game mode"
}

SETTING_OPTIONS = {
    Setting.BOARD_SIZE: [4, 6, 8, 10],
    Setting.BOARD_COLOR: ["green", "blue", "cyan", "yellow", "magenta"],
    Setting.GAME_MODE: [GameMode.LOCAL, GameMode.AI, GameMode.REMOTE]
}

'''
Thread-safe singleton settings class.
This makes sure only one settings class is instantiated so that a single state can be shared/accessed among different components,
via a single Settings instance.
'''
class Settings:
    _instance = None
    _lock = threading.Lock()

    def __init__(self):      
        if(self._initialized): return
        self.client = Client()
        if not Session().is_logged_in():
            SETTING_OPTIONS[Setting.GAME_MODE].remove(GameMode.REMOTE)
        self.state = {
            Setting.BOARD_SIZE: 4,
            Setting.BOARD_COLOR: PLAYER_COLOR[0],
            Setting.GAME_MODE: GameMode.LOCAL
        }
        self._initialized = True

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls, *args, **kwargs)
                    cls._instance._initialized = False
        return cls._instance
    
    def get_setting_label(self, setting: Setting):
        return SETTING_LABELS[setting]

    def get_setting_options(self, setting: Setting):
        return SETTING_OPTIONS[setting]

    def get_setting(self, setting: Setting):
        return self.state[setting]

    def update_settings(self, settings):
        board_size = settings[Setting.BOARD_SIZE]
        board_color = settings[Setting.BOARD_COLOR]
        game_mode = settings[Setting.GAME_MODE]
        if type(game_mode) is str:
            game_mode = GameMode.fromstring(game_mode)
        self.state = {
            Setting.BOARD_SIZE: board_size,
            Setting.BOARD_COLOR: board_color,
            Setting.GAME_MODE: game_mode
        }
        if Session().is_logged_in():
            self.client.update_settings(board_size, board_color, game_mode, Session().get_username())

    def get_board_size(self):
        return self.state[Setting.BOARD_SIZE]

    def get_board_color(self):
        return self.state[Setting.BOARD_COLOR]

    def get_game_mode(self):
        return self.state[Setting.GAME_MODE]
