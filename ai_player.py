import random
import copy

class AIPlayer:
    def __init__(self, difficulty='easy'):
        """Initialize AI with difficulty level: 'easy' (random) or 'hard' (minimax)."""
        self.difficulty = difficulty

    def make_move(self, game):
        """Make a move based on the difficulty level."""
        if self.difficulty == 'easy':
            return self._make_random_move(game)
        else :
            return self._make_minimax_move(game)
        
    def _make_random_move(self, game):
        """Make a random move from available empty cells."""
        empty_cells = game.get_empty_cells()
        if empty_cells:
            return random.choice(empty_cells)
        return None
    
    def _make_minimax_move(self, game):
        """Make the best move using the minimax algorithm."""
        empty_cells = game.get_empty_cells()
        if not empty_cells:
            return None
        
        if len(empty_cells) >= 8:
            if (1, 1) in empty_cells:
                return (1, 1)
            corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
            available_corners = [corner for corner in corners if corner in empty_cells]
            if available_corners:
                return random.choice(available_corners)
            
        best_score = float('-inf')
        best_move = None

        for row, col in empty_cells:
            game_copy = copy.deepcopy(game)
            game_copy.make_move(row, col)

            score = self._minimax(game_copy, 0, False)

            if score > best_score:
                best_score = score
                best_move = (row, col)

        return best_move
    
    def _minimax(self, game, depth, is_maximizing):
        """
        Minimax algorithm implementation.

        Args:
            game: Current game state.
            depth: Current depth in the game tree
            is_maximizing: Whether current player is maximizing or minimizing

        Returns:
            Best score for the current player
        """
        if game.winner == 'O': # Ai wins
            return 10 - depth
        elif game.winner == 'X': # player wins
            return depth - 10
        elif game.game_over: # draw
            return 0
        
        empty_cells = game.get_empty_cells()

        if is_maximizing:
            best_score = float('-inf')
            for row, col in empty_cells:
                game_copy = copy.deepcopy(game)
                game_copy.make_move(row, col)
                score = self._minimax(game_copy, depth + 1, False)
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for row, col in empty_cells:
                game_copy = copy.deepcopy(game)
                game_copy.make_move(row, col)
                score = self._minimax(game_copy, depth + 1, True)
                best_score = min(score, best_score)
            return best_score