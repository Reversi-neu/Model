from model import ReversiBoard
from view import ConsoleGameView

class GameController():
    
    def __init__(self):
        self.view = ConsoleGameView()

        width, height = self.view.get_game_size()
        self.game = ReversiBoard(width, height)

    def runGame(self):
        while self.game.game_state == 'PLAYING':
            
            game_info = self.game.game_info()
            current_board = game_info["board"]
            current_player = game_info["current_player"]
            player1_score = game_info["player1_score"]
            player2_score = game_info["player2_score"]
            self.view.printBoard(current_board, current_player)
            self.view.printMoves(self.game.possible_moves())
            
            error = False
            while error == False:
                row, col = self.view.getUserInput()
                error = self.game.make_move(col, row)

                if error == False:
                    self.view.printInvalidMove()
                    
            self.view.printScore(player1_score, player2_score)
            print()

        self.view.printBoard(current_board, current_player)
        self.view.printWinner(self.game.game_state) 

if __name__ == '__main__':
    controller = GameController()
    controller.runGame()
