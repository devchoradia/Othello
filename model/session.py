import threading
from client.client import Client

'''
Thread-safe singleton session class.
This makes sure only one Session class is instantiated so that a single login session can be shared/accessed among different components,
via a single Session instance.
'''
class Session:
    _instance = None
    _lock = threading.Lock()

    def __init__(self):      
        if(self._initialized): return
        self.username = None
        self.ELORating = None
        self._initialized = True
        self.client = Client()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls, *args, **kwargs)
                    cls._instance._initialized = False
        return cls._instance
    
    def is_logged_in(self):
        return self.username != None
    
    def log_in(self, username, ELORating):
        self.username = username
        self.ELORating = ELORating

    def log_out(self):
        self.client.logout(self.username)
        self.username = None
        self.ELORating = None
    
    def get_username(self):
        return self.username

    def get_ELORating(self):
        return self.ELORating

    def update_ELORating(self, rating):
        self.ELORating = int(rating)
