from game import Reversi
from view import ConsoleGameView

class GameController():
    
    def __init__(self):
        self.view = ConsoleGameView()

        width = self.view.get_game_size()
        self.game = Reversi(width)

    def run_game(self):
        while self.game.check_win() == False:
            
            #game_info = self.game.game_info()
            current_board = self.game.board.get_grid()
            board_size = self.game.board_size
            current_player = self.game.cur_player.value
            player1_score = self.game.player1_score
            player2_score = self.game.player2_score
            
            if len(self.game.possible_moves()) != 0:
                self.view.print_board(current_board, current_player)
                self.view.print_moves(self.game.possible_moves())
                
                error = False
                while not error:
                    row, col = self.view.get_user_input()
                    error = self.game.is_valid_move([col, row])  

                    if error == False:
                        self.view.print_invalid_move()
                        
                self.game.make_move([col, row])
                self.game.change_cur_player()

            else:
                # changing player no possible moves 
                self.game.change_cur_player()
                continue
                
            self.view.print_score(player1_score, player2_score)
            print()
            
        
        current_board = self.game.board.get_grid()
        current_player = self.game.cur_player.value
        self.view.print_board(current_board, current_player)
        self.view.print_winner(self.game.player1_score, self.game.player2_score) 

if __name__ == '__main__':
    controller = GameController()
    controller.run_game()

# 

