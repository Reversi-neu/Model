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
            self.view.printBoard(current_board, current_player)
            self.view.printMoves(self.game.possible_moves())
            
            error = False
            while error == False:
                row, col = self.view.getUserInput()
                error = self.game.make_move(col, row)

                if error == False:
                    self.view.printInvalidMove()    

        self.view.printWinner(self.game.game_state)

# X Black Score: 10         White Score: 10
# " " | " " |  
# " " | " " |  
# " " | " " |  
# " " | " " |  
# " " | " " |  
# " " | " " |  

if __name__ == '__main__':
    controller = GameController()
    controller.runGame()