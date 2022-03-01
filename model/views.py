from enum import IntEnum

class Views(IntEnum):
    LOGIN = 1
    GAME = 2
    LEADERBOARD = 3
    SETTINGS = 4
    HOME = 5

VIEW_TITLES = {
    Views.LOGIN: "Log in",
    Views.GAME: "Game",
    Views.LEADERBOARD: "Leaderboard",
    Views.SETTINGS: "Settings",
    Views.HOME: "Home"
}