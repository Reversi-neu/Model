# Reversi in Python
# Coords are formatted [y][x]
# [0][0] is top-left of board

# To-do: fix check validity to not get out of array range error

import json


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.middleTopLeft = [((width / 2) - 1), ((height / 2) - 1)]
        self.middleTopRight = [(width / 2), (height / 2) - 1]
        self.middleBottomLeft = [((width / 2) - 1), (height / 2)]
        self.middleBottomRight = [(width / 2), (height / 2)]

        self.board = []

    def make_start_board(self):
        i = 0
        j = 0
        temp_array = []

        for i in range(self.height):
            for j in range(self.width):
                temp_array.append(' ')
                j = j + 1

            self.board.append(temp_array)
            temp_array = []
            j = 0
            i = i + 1

        self.board[int((self.height / 2) - 1)][int((self.width / 2) - 1)] = 'b'
        self.board[int(self.height / 2)][int((self.width / 2) - 1)] = 'w'
        self.board[int((self.height / 2) - 1)][int(self.width / 2)] = 'w'
        self.board[int(self.height / 2)][int(self.width / 2)] = 'b'

    def print_board(self):
        i = 0

        for i in range(self.height):
            print(self.board[i])
            i = i + 1

    # Check validity of player turn and update tiles player takes with the move
    # RETURNS: false if error occurs
    # UPDATES: updates board array according to new move
    def make_turn(self, player_tile, x, y):
        # Check if move is possible (within board range and not already taken)
        if self.board[y][x] != ' ' or not self.move_on_board_check(x, y):
            return False

        # Set player selection for now
        self.board[y][x] = player_tile

        # Set enemy tile
        if player_tile == 'b':
            enemy_tile = 'w'
        elif player_tile == 'w':
            enemy_tile = 'b'
        else:
            return False

        for x_dir, y_dir in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
            x_pos, y_pos = x, y
            x_pos += x_dir
            y_pos += y_dir

            if not self.move_on_board_check(x, y):
                continue

            while self.board[y_pos][x_pos] == enemy_tile:
                x_pos += x_dir
                y_pos += y_dir

                if not self.move_on_board_check(x, y):
                    continue

    def move_on_board_check(self, x, y):
        return 0 <= x <= self.width - 1 and 0 <= y <= self.height - 1

    # def check_win(self):


game_width = 8
game_height = 8

board = Board(game_width, game_height)
board.make_start_board()

output = board.make_turn('b', 2, 2)
board.print_board()
print(output)

# event_json = json(player, move_x, move_y)
# response_json = json(tile_states)
# output_json.player = player
# output_json.move_x = move_x
