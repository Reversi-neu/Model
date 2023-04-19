from abc import ABC, abstractmethod

class GamePrototype(ABC):
    @abstractmethod
    def copy(self):
        pass