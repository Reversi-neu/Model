# Reversi in Python
# Coords are formatted [y][x]
# [0][0] is top-left of board

# To-do: weird bug on test moves to fix

import json


class Board:
    def __init__(self, width=8, height=8):
        self.width = width
        self.height = height

        self.middleTopLeft = [((width / 2) - 1), ((height / 2) - 1)]
        self.middleTopRight = [(width / 2), (height / 2) - 1]
        self.middleBottomLeft = [((width / 2) - 1), (height / 2)]
        self.middleBottomRight = [(width / 2), (height / 2)]

        self.board = []

    def import_board(self, user_board):
        for i in range(self.height):
            self.board.append(user_board[i])

    def make_start_board(self):
        i = 0
        j = 0
        temp_array = []

        for i in range(self.height):
            for j in range(self.width):
                temp_array.append(' ')
                j += 1

            self.board.append(temp_array)
            temp_array = []
            j = 0
            i += 1

        self.board[int((self.height / 2) - 1)][int((self.width / 2) - 1)] = 'b'
        self.board[int(self.height / 2)][int((self.width / 2) - 1)] = 'w'
        self.board[int((self.height / 2) - 1)][int(self.width / 2)] = 'w'
        self.board[int(self.height / 2)][int(self.width / 2)] = 'b'

    def print_board(self):
        i = 0

        for i in range(self.height):
            print(self.board[i])
            i += 1

    # Check validity of player turn and update tiles player takes with the move
    # RETURNS: false if error occurs
    # UPDATES: updates board array according to new move
    def make_turn(self, player, x, y):
        # Check if move is possible (within board range and not already taken)
        if not self.move_on_board_check(x, y) or self.board[y][x] != ' ':
            return False

        # Set player selection for now
        self.board[y][x] = player

        # Set enemy tile
        if player == 'b':
            enemy = 'w'
        elif player == 'w':
            enemy = 'b'
        else:
            self.board[y][x] = ' '  # Resets player selection
            return False

        tile_changes = []

        # Check what tiles need to be changed in all 8 directions from selection
        for x_dir, y_dir in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
            x_pos, y_pos = x, y
            x_pos += x_dir
            y_pos += y_dir

            if not self.move_on_board_check(x, y):
                continue

            while self.board[y_pos][x_pos] == enemy:
                x_pos += x_dir
                y_pos += y_dir

                if not self.move_on_board_check(x, y):
                    break
                    
            if self.board[y_pos][x_pos] == player:
                while x_pos != (x-1) and y_pos != (y-1):
                    x_pos -= x_dir
                    y_pos -= y_dir

                    tile_changes.append([player, x_pos, y_pos])

        # If no tile changes then the move is invalid
        if len(tile_changes) == 0:
            self.board[y][x] = ' '
            return False

        for tile in tile_changes:
            self.board[tile[2]][tile[1]] = tile[0]

        return tile_changes

    def move_on_board_check(self, x, y):
        return 0 <= x <= self.width - 1 and 0 <= y <= self.height - 1

    def clone_board(self):
        return self.board

    # def check_win(self):


game_width = 8
game_height = 8

board = Board(game_width, game_height)
board.make_start_board()
board.print_board()
print("\n")

output = board.make_turn('b', 3, 5)
board.print_board()
print(output)

output = board.make_turn('w', 2, 5)
board.print_board()
print(output)

output = board.make_turn('b', 2, 4)
board.print_board()
print(output)

output = board.make_turn('w', 2, 5)
board.print_board()
print(output)

# event_json = json(player, move_x, move_y)
# response_json = json(tile_states)
# output_json.player = player
# output_json.move_x = move_x   
