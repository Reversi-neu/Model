# Reversi AI class - AI implementation for Reversi game
class ReversiAI:
    """
    An AI agent for the reversi game using minimax
    
    Attributes
    ----------
    depth : int
        the depth of search for the ai algo
        
    Methods
    -------
    get_best_move(game)
        Gets the best next move for the current game
    minimax(game, depth, maximizing)
        In charge of the minimax algorithm and scoring moves
    """
    
    def __init__(self, depth):
        self.depth = depth

    # Returns the best move for the AI
    def get_best_move(self, game):
        """
        Gets the best move using minimax
        
        Parameters
        ----------
            game : Reversi
                The game object for the AI to run on
        
        Returns
        -------
            bestMove : int[2]
                A coordinate of the best next move according
                to the AI
        """
        
        possibleMoves = game.possibleMoves()
        if not possibleMoves:
            return None

        bestMove = None
        bestScore = float('-inf')

        for move in possibleMoves:
            newGame = game.copy()
            newGame.makeMove(move)
            newGame.changeCurPlayer()
            newGame.checkWin()

            score = self.minimax(newGame, self.depth, False)

            print(f"Move: {move}, Score: {score}")

            if score > bestScore:
                bestScore = score
                bestMove = move

        return bestMove

    # Minimax algorithm for AI - returns the best score for the AI
    def minimax(self, game, depth, maximizing):
        """
        Runs the minimax algorithm
        
        Parameters
        ----------
            game : Reversi
                The game object for the AI to run on
            depth : int
                How deep the algorithm will search 
            maximizing : boolean
                What type of scoring is happening, mini or max
        
        Returns
        -------
            minEval : int
                Lowest score turn found if minimizing
            maxEval : int
                Highest score turn found if maximizing
        """
        
        if depth == 0 or game.checkWin():
            if game.curPlayer == 1:
                return game.player1Score - game.player2Score
            else:
                return game.player2Score - game.player1Score

        if maximizing:
            maxEval = float('-inf')
            
            for move in game.possibleMoves():
                newGame = game.copy()
                newGame.makeMove(move)
                newGame.changeCurPlayer()
                newGame.checkWin()
                
                eval = self.minimax(newGame, depth-1, False)
                maxEval = max(maxEval, eval)

            return maxEval

        else:
            minEval = float('inf')

            for move in game.possibleMoves():
                newGame = game.copy()
                newGame.makeMove(move)
                newGame.changeCurPlayer()
                newGame.checkWin()
                
                eval = self.minimax(newGame, depth-1, True)
                minEval = min(minEval, eval)

            return minEval
