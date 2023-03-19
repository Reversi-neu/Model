class ReversiAI:
    def __init__(self, depth):
        self.depth = depth

    def get_best_move(self, game):
        possible_moves = game.possible_moves()
        if not possible_moves:
            return None

        best_move = None
        best_score = float('-inf')

        for move in possible_moves:
            new_game = game.copy(game.board_size)
            new_game.make_move(move)
            new_game.change_cur_player()
            new_game.check_win()

            score = self.minimax(new_game, self.depth, False)

            print(f"Move: {move}, Score: {score}")

            if score > best_score:
                best_score = score
                best_move = move

        return best_move

        #print(possible_moves)
        #print(game.board.get_grid())
        #print(game.player1_score)
        #print(game.player2_score)

        #return possible_moves[0]

    def minimax(self, game, depth, maximizing):
        if depth == 0 or game.check_win():
            if game.cur_player == 1:
                return game.player1_score - game.player2_score
            else:
                return game.player2_score - game.player1_score

        if maximizing:
            max_eval = float('-inf')
            
            for move in game.possible_moves():
                new_game = game.copy(game.board_size)
                new_game.make_move(move)
                new_game.change_cur_player()
                new_game.check_win()
                
                eval = self.minimax(new_game, depth-1, False)
                max_eval = max(max_eval, eval)

            return max_eval

        else:
            min_eval = float('inf')

            for move in game.possible_moves():
                new_game = game.copy(game.board_size)
                new_game.make_move(move)
                new_game.change_cur_player()
                new_game.check_win()
                
                eval = self.minimax(new_game, depth-1, True)
                min_eval = min(min_eval, eval)

            return min_eval
