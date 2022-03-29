import threading
from model.player import PLAYER_COLOR
from enum import IntEnum, Enum

class GameMode(Enum):
    def __str__(self):
        return str(self.value)

    @classmethod
    def fromstring(cls, str):
        return getattr(cls, str.upper(), None)

    LOCAL = "local"
    AI = "AI"
    REMOTE = "remote"

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
    Setting.GAME_MODE: [GameMode.LOCAL, GameMode.AI]
}

class SettingsBaseClass:
    state = {
        Setting.BOARD_SIZE: 4,
        Setting.BOARD_COLOR: PLAYER_COLOR[0],
        Setting.GAME_MODE: GameMode.LOCAL
    }
    
    def get_setting_label(self, setting: Setting):
        return SETTING_LABELS[setting]

    def get_setting_options(self, setting: Setting):
        return SETTING_OPTIONS[setting]

    def get_setting(self, setting: Setting):
        return self.state[setting]

    def update_setting(self, setting: Setting, value):
        if setting == Setting.GAME_MODE and type(value) is str:
            value = GameMode.fromstring(value)
        if value not in SETTING_OPTIONS[setting]:
            print("Attempted to set " + SETTING_LABELS[setting] + " as " + str(value))
            return
        self.state.update({
            setting: value
        })

    def get_board_size(self):
        return self.state[Setting.BOARD_SIZE]

    def get_board_color(self):
        return self.state[Setting.BOARD_COLOR]

    def get_game_mode(self):
        return self.state[Setting.GAME_MODE]

'''
Thread-safe singleton settings class
'''
class Settings(SettingsBaseClass):
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance