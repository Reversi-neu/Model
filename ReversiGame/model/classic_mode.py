from model.game_logic import GameLogic

class ClassicMode(GameLogic):
    DIRECTIONS = [[0, 1], [1, 1], [1, 0], [1, -1],
                  [0, -1], [-1, -1], [-1, 0], [-1, 1]]

    def __init__(self):
        self.size = 8

    def get_size(self, s):
        self.size = s

    def is_move_on_board(self, x, y):
        return 0 <= x < self.size and 0 <= y < self.size

    def is_move_possible(self, board, move, player):
        x, y = move

        # Check if move is on the board
        if not self.is_move_on_board(x, y):
            return False

        # Check if tile picked is empty
        if not board[y][x] == 0 or "":
            return False

        # Check tiles in all directions from selection
        for x_dir, y_dir in self.DIRECTIONS:
            x_pos, y_pos = x, y
            x_pos += x_dir
            y_pos += y_dir

            # Check if tile is on board 
            if not self.is_move_on_board(x_pos, y_pos):
                continue 

            # Check if next tile is an enemy
            if board[y_pos][x_pos] == player:
                continue

            # Continues while still enemies
            while board[y_pos][x_pos] == 3-player:
                x_pos += x_dir
                y_pos += y_dir

                # Check if tile is on board
                if not self.is_move_on_board(x_pos, y_pos):
                    break

                # Check if next tile is an enemy
                if board[y_pos][x_pos] == player:
                    return True

        return False

    def make_move(self, board, move, player):
        x, y = move
    
        # Store gained tiles before checking in every dir
        gained_tiles = []
        for x_dir, y_dir in self.DIRECTIONS:
            x_pos, y_pos = x, y
            x_pos += x_dir
            y_pos += y_dir

            # Jump over enemy tiles
            temp_array = []
            if self.is_move_on_board(x_pos, y_pos):
                while board[y_pos][x_pos] == 3-player:
                    temp_array.append([x_pos, y_pos])
                    x_pos += x_dir
                    y_pos += y_dir

                    # Check if tile is on board
                    if not self.is_move_on_board(x_pos, y_pos):
                        break

                # Player tile after enemy tiles
                if self.is_move_on_board(x_pos, y_pos):
                    if board[y_pos][x_pos] == player:
                        for tiles in temp_array:
                            gained_tiles.append(tiles)  # Taken tile found



        gained_tiles.append([x, y])     # Original move
        return gained_tiles

    def possible_moves(self, board, player):
        moves = []

        for i in range(self.size):
            for j in range(self.size):
                if self.is_move_possible(board, [i, j], player):
                    moves.append([i, j])

        return moves

    def check_win(self, board):
        # Check if current player has no possible moves
        return not self.possible_moves(board, 1) and not self.possible_moves(board, 2)

    
