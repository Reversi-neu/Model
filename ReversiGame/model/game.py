from model.player import Player
from model.board import Board
from model.classic_mode import ClassicMode
from model.reversi_interface import ReversiInterface

class Reversi(ReversiInterface):
    # ai_depth 0 means no AI in game
    def __init__(self, size=8, game_logic=ClassicMode()): 
        self.board = Board(size, board=[])
        self.board_size = size
        self.cur_player = Player.black
        self.game_logic = game_logic
        self.player1_score = 2
        self.player2_score = 2

        self.game_logic.get_size(size)

        self.board.__setitem__([int(size / 2) - 1, int((size / 2) - 1)], Player.black.value)
        self.board.__setitem__([int((size / 2) - 1), int(size / 2)], Player.white.value)
        self.board.__setitem__([int(size / 2), int((size / 2) - 1)], Player.white.value)
        self.board.__setitem__([int(size / 2), int(size / 2)], Player.black.value)

    def is_valid_move(self, move):
        # returns False if not valid
        return self.game_logic.is_move_possible(self.board.get_grid(), move, self.cur_player.value)
    
    def make_move(self, move):
        gained_tiles = self.game_logic.make_move(self.board.get_grid(), move, self.cur_player.value)

        for tile in gained_tiles:
            self.board.__setitem__(tile, self.cur_player.value)
    
    def change_cur_player(self):
        if self.cur_player == Player.black:
            self.cur_player = Player.white
        else:
            self.cur_player = Player.black
    
    def check_win(self):
        self.player1_score = 0
        self.player2_score = 0
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board.__getitem__([i, j]) == 1:
                    self.player1_score += 1
                elif self.board.__getitem__([i, j]) == 2:
                    self.player2_score += 1

        # string of game state
        return  self.game_logic.check_win(self.board.get_grid())


    def possible_moves(self):
        # array of moves [0, 0]
        return self.game_logic.possible_moves(self.board.get_grid(), self.cur_player.value)

    # DESIGN PATTERN: Prototype
    def copy(self):
        copied_game = Reversi(self.board_size, self.game_logic)
        copied_game.board = Board(self.board_size, board=[row.copy() for row in self.board.get_grid()])
        copied_game.cur_player = self.cur_player
        copied_game.player1_score = self.player1_score
        copied_game.player2_score = self.player2_score
        return copied_game
