import json

class Player:
    def __init__(self, color):
        self.color = color
        self.score = 0

class ReversiBoard:
    BLACK = 'b'
    WHITE = 'w'
    EMPTY = ' '

    DIRECTIONS = [[0, 1], [1, 1], [1, 0], [1, -1],
                  [0, -1], [-1, -1], [-1, 0], [-1, 1]]

    def __init__(self, width=8, height=8):
        self.width = width
        self.height = height

        # Set players and colors
        self.player1 = Player(self.BLACK)
        self.player2 = Player(self.WHITE)

        # Start game as black
        self.cur_player = self.player1
        self.cur_enemy = self.player2

        self.game_state = 'PLAYING'

        # Create the board matrix
        self.board = []

        for i in range(height):
            self.board.append([' '] * width)

        # Place starting tiles
        self.board[int((height / 2) - 1)][int((width / 2) - 1)] = self.player1.color
        self.board[int(height / 2)][int((width / 2) - 1)] = self.player2.color
        self.board[int((height / 2) - 1)][int(width / 2)] = self.player2.color
        self.board[int(height / 2)][int(width / 2)] = self.player1.color

    # Prints board to console
    def print_board(self):
        for i in range(self.height):
            print(self.board[i])

    # Changes current active player
    def change_cur_player(self):
        if self.cur_player == self.player1:
            self.cur_player = self.player2
            self.cur_enemy = self.player1
        else:
            self.cur_player = self.player1
            self.cur_enemy = self.player2

    # Check position is within range of board
    def is_move_on_board(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    # Check is user move is valid
    def is_move_possible(self, x, y):
        # Check if move is on the board
        if not self.is_move_on_board(x, y):
            return False

        # Check if tile picked is empty
        if not self.board[y][x] == ' ':
            return False

        # Check tiles in all directions from selection
        for x_dir, y_dir in self.DIRECTIONS:
            x_pos, y_pos = x, y
            x_pos += x_dir
            y_pos += y_dir

            # Check if next tile in board and enemy
            if self.board[y_pos][x_pos] == self.cur_player.color or \
                    not self.is_move_on_board(x_pos, y_pos):
                continue

            # Continues while still enemies
            while self.board[y_pos][x_pos] == self.cur_enemy.color:
                x_pos += x_dir
                y_pos += y_dir

                # Valid move found
                if self.board[y_pos][x_pos] == self.cur_player.color:
                    return True

        return False    # No valid move found

    def make_move(self, x, y):
        # Check if game is playing and move is legal
        if self.game_state != 'PLAYING':
            return False
        if not self.is_move_possible(x, y):
            return False

        # Store gained tiles before checking in every dir
        gained_tiles = []
        for x_dir, y_dir in self.DIRECTIONS:
            x_pos, y_pos = x, y
            x_pos += x_dir
            y_pos += y_dir

            # Jump over enemy tiles
            temp_array = []
            while self.board[y_pos][x_pos] == self.cur_enemy.color:
                temp_array.append([x_pos, y_pos])
                x_pos += x_dir
                y_pos += y_dir

            # Player tile after enemy tiles
            if self.board[y_pos][x_pos] == self.cur_player.color:
                for tiles in temp_array:
                    gained_tiles.append(tiles)  # Taken tile found

        gained_tiles.append([x, y]) # Original move
        print(gained_tiles)
        # Set tiles on board
        for tiles in gained_tiles:
            self.board[tiles[1]][tiles[0]] = self.cur_player.color

        # Calculates score of each player after move
        temp_score1 = 0
        temp_score2 = 0
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] == 'b':
                    temp_score1 += 1
                if self.board[i][j] == 'w':
                    temp_score2 += 1
        self.player1.score = temp_score1
        self.player2.score = temp_score2

        # Check games state and change player turn
        self.game_state = self.check_game_state()
        self.change_cur_player()

    #def check_game_state(self):



testBoard = ReversiBoard()
testBoard.print_board()
result = testBoard.make_move(3, 5)
print(result)
testBoard.print_board()
print(testBoard.player1.score)
print(testBoard.player2.score)

result = testBoard.make_move(2, 5)
print(result)
testBoard.print_board()
print(testBoard.player1.score)
print(testBoard.player2.score)

result = testBoard.make_move(4, 2)
print(result)
testBoard.print_board()
print(testBoard.player1.score)
print(testBoard.player2.score)
