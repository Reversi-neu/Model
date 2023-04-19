from model.player import Player

# Board class, holds the board and the size of the board
class Board:
    """
    A class to hold the game board.
    ...
    
    Attributes
    ----------
    size : int
        size of the board
    board : int[]
        the board grid itself
        
    Methods
    -------
    __getitem__(coordinate)
        Gets item from coord
    __setitem__(coordinate)
        Sets item at coord
    getGrid()
        Returns the board grid
    """
    
    def __init__(self, size, board=[]):
        """
        Constructs the game board and stores it
        
        Parameters
        ----------
            size : int
                Size of board
            board : int[]
                Board array, can be empty
        """
        self.size = size
        self.board = board

        if self.board == []:
            for i in range(size):
                self.board.append([0] * size)

    def __getitem__(self, coordinate):
        """
        Returns the value on the grid at the given coord
        
        Parameters
        ----------
            coordinate : int[2]
                Coordinate array
        """
        return self.board[coordinate[1]][coordinate[0]]

    def __setitem__(self, coordinate, player: Player):
        """
        Sets the value on the grid at the given coord to given color
        
        Parameters
        ----------
            coordinate : int[2]
                Coordinate array
            player : Player()
                Player object
        """
        self.board[coordinate[1]][coordinate[0]] = player

    def getGrid(self):
        """
        Returns the entire grid array
        
        Parameters
        ----------
        """
        return self.board
