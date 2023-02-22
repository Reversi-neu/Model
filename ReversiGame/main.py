# Reversi (Othello) Model
# Coordinates are [0,0] in the top left of the board

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

            # Check if tile is on board
            if not self.is_move_on_board(x_pos, y_pos):
                continue

            # Check if next tile is an enemy
            if self.board[y_pos][x_pos] == self.cur_player.color:
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
            if self.is_move_on_board(x_pos, y_pos):
                while self.board[y_pos][x_pos] == self.cur_enemy.color:
                    temp_array.append([x_pos, y_pos])
                    x_pos += x_dir
                    y_pos += y_dir

                    if not self.is_move_on_board(x_pos, y_pos):
                        break

                # Player tile after enemy tiles
                if self.is_move_on_board(x_pos, y_pos):
                    if self.board[y_pos][x_pos] == self.cur_player.color:
                        for tiles in temp_array:
                            gained_tiles.append(tiles)  # Taken tile found

        gained_tiles.append([x, y])     # Original move
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

    def possible_moves(self):
        moves = []

        for i in range(self.height):
            for j in range(self.width):
                if self.is_move_possible(j, i):
                    moves.append([j, i])

        return moves

    def check_game_state(self):
        # Check if current player has no possible moves
        if len(self.possible_moves()) == 0:
            self.change_cur_player()

            # Check if next player has no possible moves
            if not self.possible_moves():
                # Change the game state
                if self.player1.score > self.player2.score:
                    return 'BLACK_WIN'
                elif self.player2.score > self.player1.score:
                    return 'WHITE_WIN'
                else:
                    return 'TIE'

        # Game is still active and players have moves
        return 'PLAYING'

    def game_info(self):
        color_map = {
            "b": "player1",
            "w": "player2"
        }
        return {
            "board": self.print_board(),
            "current_player": color_map[self.cur_player.color],
            "game_state": self.game_state,
            "player1_score": self.player1.score,
            "player2_score": self.player2.score
        }
