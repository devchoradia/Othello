from enum import Enum

class GameMode(Enum):
    def __str__(self):
        return str(self.value)

    @classmethod
    def fromstring(cls, str):
        return getattr(cls, str.upper(), None)

    LOCAL = "local"
    AI = "AI"
    REMOTE = "remote"
