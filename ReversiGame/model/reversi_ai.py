from model.classic_mode import ClassicMode

class ReversiAI:
    def __init__(self, depth):
        self.depth = depth

    def get_best_move(self, board, cur_player, reversi_instance, board_size=8, game_logic=ClassicMode()):
        possible_moves = self.possible_moves(board, cur_player)
        if not possible_moves:
            return None

        best_move = None
        best_score = float('-inf')

        for move in possible_moves:
            new_board = [row.copy() for row in board]
            new_game = reversi_instance.copy()
            new_game.cur_player = cur_player
            new_game.make_move(move)
            #print(new_game.board.get_grid())
            new_game.check_win()
            new_game.change_cur_player()

            score = self.minimax(new_game, self.depth, False)

            #print(f"Move: {move}, Score: {score}")

            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    def minimax(self, game, depth, maximizing_player):
        #print(game.player1_score)
        #print(game.player2_score)
        if depth == 0 or game.check_win():
            if game.cur_player == 1:
                return game.player1_score - game.player2_score
            else:
                return game.player2_score - game.player1_score

        if maximizing_player:
            max_eval = float('-inf')
            for move in game.possible_moves():
                new_board = game.board.copy()
                new_game = game.__class__(game.board_size, game.game_logic)
                new_game.board = new_board
                new_game.cur_player = game.cur_player
                new_game.make_move(move)
                new_game.check_win()
                new_game.change_cur_player()

                eval = self.minimax(new_game, depth - 1, False)
                max_eval = max(max_eval, eval)

            return max_eval
        else:
            min_eval = float('inf')
            for move in game.possible_moves():
                new_board = game.board.copy()
                new_game = game.__class__(game.board_size, game.game_logic)
                new_game.board = new_board
                new_game.cur_player = game.cur_player
                new_game.make_move(move)
                new_game.check_win()
                new_game.change_cur_player()

                eval = self.minimax(new_game, depth - 1, True)
                min_eval = min(min_eval, eval)

            return min_eval

    def possible_moves(self, board, player):
        game_logic = ClassicMode()
        game_logic.get_size(len(board))
        moves = []

        for i in range(len(board)):
            for j in range(len(board)):
                if game_logic.is_move_possible(board, [i, j], player):
                    moves.append([i, j])

        return moves
