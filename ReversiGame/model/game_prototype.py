from abc import ABC, abstractmethod

# Interface for game prototype
class GamePrototype(ABC):
    """
    Prototype interface for the game object
    
    Methods
    -------
    copy()
        creates a copy of the game object
    """
    
    @abstractmethod
    def copy(self):
        """
        Creates a copy of the object
        """
        
        pass
