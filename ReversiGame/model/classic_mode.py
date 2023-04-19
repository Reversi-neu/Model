from model.game_logic import GameLogic

# Classic mode game logic, inherits from GameLogic
class ClassicMode(GameLogic):
    """
    A concrete implementation of the interface class for 
    the appropriate game rules.
    
    Attributes
    ----------
    size : int
        Size of the board
        
    Methods
    -------
    getSize(s):
        Gets the size of the game board
    isMoveOnBoard(x, y):
        Checks if move is within board boundaries
    isMovePossible(board, move, player):
        Checks if move made is legal
    makeMove(board, move, player):
        Makes a move on the board and updates the tiles
    possibleMoves(board, player):
        Returns array of possible moves for the player
    """
    
    DIRECTIONS = [[0, 1], [1, 1], [1, 0], [1, -1],
                  [0, -1], [-1, -1], [-1, 0], [-1, 1]]

    def __init__(self):
        self.size = 8

    def getSize(self, s):
        """
        Gets the size of the board
        
        Parameters
        ----------
        s : int
            Size of the board
        """
        
        self.size = s

    def isMoveOnBoard(self, x, y):
        """
        Checks if move is within board boundaries
        
        Parameters
        ----------
        x: int
            X pos of move
        y: int
            Y pos of move
            
        Returns
        -------
        boolean :
            True on legal move
        """
        
        return 0 <= x < self.size and 0 <= y < self.size

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
        
        x, y = move

        # Check if move is on the board
        if not self.isMoveOnBoard(x, y):
            return False

        # Check if tile picked is empty
        if not board[y][x] == 0 or "":
            return False

        # Check tiles in all directions from selection
        for xDir, yDir in self.DIRECTIONS:
            xpos, ypos = x, y
            xpos += xDir
            ypos += yDir

            # Check if tile is on board 
            if not self.isMoveOnBoard(xpos, ypos):
                continue 

            # Check if next tile is an enemy
            if board[ypos][xpos] == player:
                continue

            # Continues while still enemies
            while board[ypos][xpos] == 3-player:
                xpos += xDir
                ypos += yDir

                # Check if tile is on board
                if not self.isMoveOnBoard(xpos, ypos):
                    break

                # Check if next tile is an enemy
                if board[ypos][xpos] == player:
                    return True

        return False

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
            
        Returns
        -------
        gainedTiles : int[]
            Array of the tiles gained by the players move
        """
        
        x, y = move
    
        # Store gained tiles before checking in every dir
        gainedTiles = []
        for xDir, yDir in self.DIRECTIONS:
            xpos, ypos = x, y
            xpos += xDir
            ypos += yDir

            # Jump over enemy tiles
            tempArray = []
            if self.isMoveOnBoard(xpos, ypos):
                while board[ypos][xpos] == 3-player:
                    tempArray.append([xpos, ypos])
                    xpos += xDir
                    ypos += yDir

                    # Check if tile is on board
                    if not self.isMoveOnBoard(xpos, ypos):
                        break

                # Player tile after enemy tiles
                if self.isMoveOnBoard(xpos, ypos):
                    if board[ypos][xpos] == player:
                        for tiles in tempArray:
                            gainedTiles.append(tiles)  # Taken tile found



        gainedTiles.append([x, y])     # Original move
        return gainedTiles

    def possibleMoves(self, board, player):
        """
        Returns list of possible player moves
        
        Parameters
        ----------
        board : int[]
            Board array
        player : int
            Current player turn
            
        Returns
        -------
        moves : int[]
            Array of legal move coordinates
        """
        
        moves = []

        for i in range(self.size):
            for j in range(self.size):
                if self.isMovePossible(board, [i, j], player):
                    moves.append([i, j])

        return moves

    def checkWin(self, board):
        """
        Checks the state of the game and for a win
        
        Parameters
        ----------
        board : int[]
            Board array
            
        Returns
        -------
        boolean :
            True on game end
        """
        
        # Check if current player has no possible moves
        return not self.possibleMoves(board, 1) and not self.possibleMoves(board, 2)

    
