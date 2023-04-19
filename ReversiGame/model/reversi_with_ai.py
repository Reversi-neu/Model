from model.reversi_interface import ReversiInterface
from model.reversi_ai import ReversiAI
import copy

# ReversiAIProxy class - used for design pattern proxy and AI implementation
class ReversiAIProxy(ReversiInterface):
    """
    The reversi game AI proxy class
    
    Attributes
    ----------
    reversi : Reversi()
        Stores the object this class is proxying
    ai_depth : int
        Stores the depth of search for the AI
        
    Methods
    -------
    get_ai_move():
        Gets the best move for the next player on the current game 
        from the AI
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
    
    def __init__(self, reversi, ai_depth=0):
        self.reversi = reversi
        if ai_depth != 0:
            self.ai = ReversiAI(ai_depth)

    def get_ai_move(self):
        self.reversi.checkWin()
        return self.ai.get_best_move(self.reversi.copy())

    def isValidMove(self, move):
        """
        Returns if a move is valid or not
        
        Parameters
        ----------
        move : int[]
            Coordinate of the move
            
        Returns
        -------
        boolean : is the turn valid
        """
        
        return self.reversi.isValidMove(move)

    def makeMove(self, move):
        """
        Makes a move on the board according the the gamelogic and the given move
        
        Parameters
        ----------
        move : int[]
            Coordinate of the move
        """
        
        return self.reversi.makeMove(move)

    def changeCurPlayer(self):
        """
        Changes the current player to the next one
        """
        
        return self.reversi.changeCurPlayer()

    def checkWin(self):
        """
        Checks if the game is over
            
        Returns
        -------
        str : state of the game
        """
        
        return self.reversi.checkWin()

    def possibleMoves(self):
        """
        Checks all of the possible moves for the current player
            
        Returns
        -------
        int[] : array of legal move coordinate
        """
        
        return self.reversi.possibleMoves()

    def copy(self):
        """
        Create a copy of the current game object.
            
        Returns
        -------
        Reversi() : Returns a copy of this game object
        """
        
        return self.reversi.copy()

    def __getattr__(self, attr):
        if attr == '__deepcopy__':
            return lambda memo: copy.deepcopy(self.reversi, memo)
        return getattr(self.reversi, attr)

