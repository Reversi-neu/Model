from flask import Flask
from model import ReversiBoard
from view import ConsoleGameView

app = Flask(__name__)



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
