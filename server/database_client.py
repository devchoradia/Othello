from mysql.connector import connect, Error
from enum import Enum
import json
from json import JSONEncoder
from model.player.player import Player
from model.game_mode import GameMode
import numpy

# https://pynative.com/python-serialize-numpy-ndarray-into-json/
# To store game state to database
class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)

class LOGIN_RESULT(Enum):
    SUCCESS = 1
    INVALID_USER = 2
    INVALID_PASSWORD = 3
    UNKNOWN_ERROR = 4

LOGIN_RESULT_MESSAGE = {
    LOGIN_RESULT.SUCCESS: "Success logging in", 
    LOGIN_RESULT.INVALID_USER: "This username doesn't exist", 
    LOGIN_RESULT.INVALID_PASSWORD: "Invalid password", 
    LOGIN_RESULT.UNKNOWN_ERROR: "An unknown error occurred"
}

class REGISTER_RESULT(Enum):
    SUCCESS = 1
    USER_EXISTS = 2
    INVALID_INPUT = 3
    UNKNOWN_ERROR = 4


REGISTER_RESULT_MESSAGE = {
    REGISTER_RESULT.SUCCESS: "Success registering account",
    REGISTER_RESULT.USER_EXISTS: "This username already exists",
    REGISTER_RESULT.INVALID_INPUT: "Invalid username or password input",
    REGISTER_RESULT.UNKNOWN_ERROR: "An unknown error occurred"
}

class DatabaseClient:
    def __init__(self):
        self.host = "localhost"
        self.username = "team2"
        self.password = "password123!"
        self.database = "reversi"
        # self.set_up_database()

    def set_up_database(self):
        skip_database_config = input("Proceed with local database configuration? [Y/N]: ")
        if (skip_database_config != "N" and skip_database_config != "n"):
            self.host = input("Enter local database host: ")
            self.username = input("Enter username: ")
            self.password = input("Enter password: ")

    def make_connection(self):
        try:
            conn = connect(
                host=self.host,
                username=self.username,
                password=self.password,
                database=self.database)
        except Error as e:
            print(e)
        return conn

    def register_user(self, username, password):
        user_info = (username, 0)
        if not username or not password:
            return REGISTER_RESULT.INVALID_INPUT, user_info
        insert = """
            INSERT into users (username, password) VALUES(%s, %s);
        """
        register_result = REGISTER_RESULT.UNKNOWN_ERROR
        if self.does_user_exist(username):
            return REGISTER_RESULT.USER_EXISTS, user_info
        conn = self.make_connection()
        args = (username, password)
        try: 
            with conn.cursor() as cursor:
                cursor.execute(insert, args)
                conn.commit()
                register_result = REGISTER_RESULT.SUCCESS
        except Error as e:
            print(e)
        finally:
            conn.close()
        return register_result, user_info
    
    def does_user_exist(self, username):
        conn = self.make_connection()
        does_user_exist_query = """
            SELECT username from users WHERE username=%s;
        """
        does_user_exist = None
        try:
            with conn.cursor() as cursor:
                cursor.execute(does_user_exist_query, (username,))
                result = cursor.fetchall()
                does_user_exist = len(result) != 0
        finally:
            conn.close()
        return does_user_exist

    def login(self, username, password):
        conn = self.make_connection()
        args = (username, password)
        ELORating = None
        login_result = LOGIN_RESULT.UNKNOWN_ERROR
        get_user_info_query = """
            SELECT username, ELORating from users WHERE username=%s AND password=%s;
        """
        try:
            with conn.cursor() as cursor:
                cursor.execute(get_user_info_query, args)
                result = cursor.fetchall()
                if len(result) == 0:
                    login_result = LOGIN_RESULT.INVALID_USER if not self.does_user_exist(username) else LOGIN_RESULT.INVALID_PASSWORD
                else:
                    login_result = LOGIN_RESULT.SUCCESS
                    ELORating = result[0][1]
        finally:
            conn.close()
        return login_result, (username, ELORating)

    def get_leaderboard(self, count=10):
        conn = self.make_connection()
        query = f"SELECT username, ELORating FROM users ORDER BY ELORating DESC LIMIT {count};"
        try:
            with conn.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
        finally:
            conn.close()
        return result

    def update_rating(self, rating, username):
        conn = self.make_connection()
        statement = """
            UPDATE users set ELORating = %s where username = %s;
        """
        args = (rating, username)
        try:
            with conn.cursor() as cursor:
                cursor.execute(statement, args)
                result = cursor.fetchall()
        finally:
            conn.close()
        return result

    def update_game_state(self, board, current_player, username):
        conn = self.make_connection()
        statement = """
            UPDATE users set gameState = %s, currentPlayer = %s where username = %s;
        """
        numpyData = {"board": board}
        encodedBoard = json.dumps(numpyData, cls=NumpyArrayEncoder)
        args = (encodedBoard, int(current_player), username)
        try:
            with conn.cursor() as cursor:
                cursor.execute(statement, args)
                conn.commit()
        finally:
            conn.close()

    def remove_game_state(self, username):
        conn = self.make_connection()
        statement = """
            UPDATE users set gameState = NULL, currentPlayer = NULL where username = %s;
        """
        try:
            with conn.cursor() as cursor:
                cursor.execute(statement, (username,))
                conn.commit()
        finally:
            conn.close()

    def get_game_state(self, username):
        conn = self.make_connection()
        statement = """
            SELECT gameState, currentPlayer from users WHERE username = %s;
        """
        try:
            with conn.cursor() as cursor:
                cursor.execute(statement, (username,))
                result = cursor.fetchall()
                if len(result) == 0:
                    print("Found no row with username " + username)
                    return None, None
                state, player_int = result[0]
                if None in result[0] and any(i is not None for i in result[0]):
                    print("Found interrupted state with missing value in database")
                    print(result[0])
                    return None, None
                if None in result[0]:
                    return None, None
                decodedState = json.loads(state)
                board = numpy.asarray(decodedState["board"])
                player = Player(player_int)
                return board, player
        finally:
            conn.close()

    def get_settings(self, username):
        conn = self.make_connection()
        statement = """
            SELECT boardSize, boardColor, gameMode from users WHERE username = %s;
        """
        try:
            with conn.cursor() as cursor:
                cursor.execute(statement, (username,))
                result = cursor.fetchall()
                if len(result) == 0:
                    print("Found no row with username " + username)
                    return None, None, None
                board_size, board_color, game_mode = result[0]
                game_mode = GameMode.fromstring(game_mode)
                return board_size, board_color, game_mode
        finally:
            conn.close()

    def update_settings(self, board_size, board_color, game_mode, username):
        conn = self.make_connection()
        statement = """
            UPDATE users set boardSize = %s, boardColor = %s, gameMode = %s where username = %s;
        """
        args = (board_size, board_color, str(game_mode), username)
        try:
            with conn.cursor() as cursor:
                cursor.execute(statement, args)
                conn.commit()
        finally:
            conn.close()