from mysql.connector import connect, Error
from enum import Enum

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
    UNKNOWN_ERROR = 3


REGISTER_RESULT_MESSAGE = {
    REGISTER_RESULT.SUCCESS: "Success registering account",
    REGISTER_RESULT.USER_EXISTS: "This username already exists",
    REGISTER_RESULT.UNKNOWN_ERROR: "An unknown error occurred"
}

class DatabaseClient:
    def __init__(self):
        self.host = "localhost"
        self.username = "team2"
        self.password = "password123!"
        self.database = "reversi"
        self.set_up_database()

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
        insert = """
            INSERT into users (username, password) VALUES(%s, %s);
        """
        register_result = REGISTER_RESULT.UNKNOWN_ERROR
        if self.does_user_exist(username):
            return REGISTER_RESULT.USER_EXISTS
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
        return register_result
    
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
