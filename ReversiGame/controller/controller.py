from flask import Flask
from model.game import Reversi
from view.view import ConsoleGameView

app = Flask(__name__)
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
                #make a game obj that contains board

        #add game obj to array games

        @app.route("/")
        def root_Web()
        # here returns the home page of the front end with possible options to login
            return "<p>Test</p>"

        @app.route("/login")
        def login(username, password)
        # if guest frontend please return null username and password. 
        # if username password empty = guest;
        # need to make another file to store userinfomation so I can referance
            return "<p>Test</p>"

        @app.route("/make_move")
        def make_move(game_ID, x_pos, y_pos, current_player)
        # check if valid move first if not valid return invalid move (is_move_possible)
        # make_move(x, y)
            return "<p>New Board as a JSON</p>"
        
        @app.route("/possible_moves")
        def possible_moves(game_ID)
        # check array games for game_ID
        # check with model possible moves possible_moves(self)
        # make JSON for front end
        # check for possible moves and return JSON of possible moves so the front end can display all possible moves by player highlighted
            return "<p>Possible Moves as a JSON</p>"

        @app.route("/game_state")# this will serve as a function to look for games
        def game_state(game_ID)
            return "<p>Game is Awaiting players, or Game Started (With players turn)</p>"

        @app.route("/create_game")# do we create games with one player and put them on a lobby for others to join, or do we create the games with the two usernames
        def create_game(player1, player2)
            return "<p>Game ID</p>"

        @app.route("/join_game")
        def join_game(game_ID, player_joining)
        # join player to game_ID and send empty board to start, also return starting player
            return "<p>Empty Board as JSON</p>"


