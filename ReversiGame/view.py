class ConsoleGameView():

    def __init__(self):
        self.width = 0
        self.height = 0

    def get_game_size(self):
        self.width = int(input("Input game width: "))
        self.height = int(input("Input game height: "))

        return self.width, self.height
        
    def printBoard(self, board, current_player):
        print("Turn:" + current_player)
        for i in range(self.height):
            print(board[i])
                
    def getUserInput(self):
        row = int(input("Input row: "))
        col = int(input("Input col: "))

        return row, col

    def printWinner(self, gameState):
        print(gameState)

    def printScore(self, player1, player2):
        print("Score:", player1, "--", player2)

    def printMoves(self, possibleMoves):
        print("Possible Moves:", possibleMoves)

    def printInvalidMove(self):
        print("Invalid move")
