from abc import ABC, abstractmethod

# Interface for Reversi game
class ReversiInterface(ABC):
    """
    An interface class to use for the game proxy
        
    Methods
    -------
    isValidMove(board, move):
        Checks if move made is legal
    makeMove(move):
        Makes a move on the board and updates the tiles
    possibleMoves():
        Returns array of possible moves for the player
    checkWin():
        Checks the state of the board
    changeCurPlayer():
        Changes the current player
    copy():
        Copies the game
    """

    @abstractmethod
    def isValidMove(self, move):
        pass

    @abstractmethod
    def makeMove(self, move):
        pass

    @abstractmethod
    def changeCurPlayer(self):
        pass

    @abstractmethod
    def checkWin(self):
        pass

    @abstractmethod
    def possibleMoves(self):
        pass

    @abstractmethod
    def copy(self):
        pass

