
from abc import ABC, abstractmethod

'''
Observer pattern
The observer (game controller) observes the observables (view and controller) by subscribing to them.
The observables notify/update the observer when important events occur
(e.g. a move is clicked on the view, the board is updated in the model, etc.)
'''
class Observer(ABC):
    def __init__(self, observables):
        for observable in observables:
            observable.add_observer(self)

    @abstractmethod
    def update(self, subject):
        pass

class Observable(ABC):
    def __init__(self):
        self.observers = set()

    def add_observer(self, observer):
        self.observers.add(observer)
    
    def remove_observer(self, observer):
        self.observers.remove(observer)
    
    def notify_observers(self):
        for observer in self.observers:
            observer.update(self)

