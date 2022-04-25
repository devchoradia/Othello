from enum import IntEnum

class Views(IntEnum):
    LOGIN = 1
    REGISTER = 2
    GAME = 3
    LEADERBOARD = 4
    SETTINGS = 5
    HOME = 6
    ONLINE_PLAYERS = 7

VIEW_TITLES = {
    Views.LOGIN: "Log in",
    Views.REGISTER: "Register",
    Views.GAME: "Game",
    Views.ONLINE_PLAYERS: "Online players",
    Views.LEADERBOARD: "Leaderboard",
    Views.SETTINGS: "Settings",
    Views.HOME: "Home"
}