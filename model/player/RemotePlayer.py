from enum import IntEnum
from model.observer import Observable
from abc import abstractmethod
from model.player.player import Player, GamePlayer
from model.session import Session

'''
Stub class for RemotePlayer class (TODO)
'''
class RemotePlayer(GamePlayer):
    def __init__(self, player_color=Player.WHITE, game=None, local_player=None, client=None):
        super().__init__(player_color)
        self.game = game
        self.local_player = local_player
        if local_player is not None:
            local_player.add_observer(self)
        self.client = client
        self.client.set_observer(self)
        self.requested_moves = []

    def get_requested_move(self) -> (int, int):
        return self.requested_moves.pop(0)
    
    def request_move(self):
        pass

    def update(self, subject, message=None):
        # Local player requested a move
        if subject == self.local_player:
            move = self.local_player.get_requested_move()
            self.client.update_remote_game(Session().get_username(), move)
        elif subject == self.client:
            self.requested_moves.append(message.body)
            # Received move from opponent
            self.notify_observers()
        