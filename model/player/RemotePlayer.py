from enum import IntEnum
from model.observer import Observable
from abc import abstractmethod
from model.player.player import Player, GamePlayer
from server.request import Request
from model.session import Session

'''
Stub class for RemotePlayer class (TODO)
'''
class RemotePlayer(GamePlayer):
    def __init__(self, player_color=Player.WHITE, local_player=None, client=None, on_opponent_disconnect=None):
        super().__init__(player_color)
        self.local_player = local_player
        if local_player is not None:
            local_player.add_observer(self)
        self.client = client
        self.client.set_observer(self)
        self.requested_moves = []
        self.on_opponent_disconnect = on_opponent_disconnect

    def get_requested_move(self) -> (int, int):
        print(self.requested_moves)
        return self.requested_moves.pop(0)
    
    def request_move(self):
        pass

    def update(self, subject, message=None):
        print("Requested moves:")
        print(self.requested_moves)
        print(message)
        # Local player requested a move
        if subject == self.local_player:
            move = self.local_player.board_view.get_requested_move()
            self.client.update_remote_game(Session().get_username(), move)
        elif subject == self.client:
            # Opponent disconnected during game
            if message.message_type == Request.OPPONENT_DISCONNECTED:
                self.on_opponent_disconnect(message.body)
            else:
                self.requested_moves.append(message.body)
                print(self.requested_moves)
                # Received move from opponent
                self.notify_observers()
        