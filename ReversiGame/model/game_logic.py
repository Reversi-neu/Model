from abc import ABC, abstractmethod

# Interface for game logic
class GameLogic(ABC):
    """
    A class interface for the game rules
    
    Attributes
    ----------
    size : int
        Size of the board
        
    Methods
    -------
    getSize(s):
        Gets the size of the game board
    isMovePossible(board, move, player):
        Checks if move made is legal
    makeMove(board, move, player):
        Makes a move on the board and updates the tiles
    possibleMoves(board, player):
        Returns array of possible moves for the player
    checkWin(board):
        Checks the state of the board
    """
    
    def __init__(self):
        self.size = 8

    @abstractmethod
    def getSize(self, s):
        """
        Gets the size of the board
        
        Parameters
        ----------
        s : int
            Size of the board
        """
        pass

    @abstractmethod
    def isMovePossible(self, board, move, player):
        """
        Checks if move is legal
        
        Parameters
        ----------
        board : int[]
            Board array
        move : int[2]
            Coordinate of the move
        player : int
            Current player turn
        """
        pass

    @abstractmethod
    def makeMove(self, board, move, player):
        """
        Makes a move and updates tiles
        
        Parameters
        ----------
        board : int[]
            Board array
        move : int[2]
            Coordinate of the move
        player : int
            Current player turn
        """
        pass

    @abstractmethod
    def possibleMoves(self, board, player):
        """
        Returns list of possible player moves
        
        Parameters
        ----------
        board : int[]
            Board array
        player : int
            Current player turn
        """
        pass

    @abstractmethod
    def checkWin(self, board):
        """
        Checks the state of the game and for a win
        
        Parameters
        ----------
        board : int[]
            Board array
        """
        pass

    
