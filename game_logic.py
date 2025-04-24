class TicTacToe:
    def __init__(self):
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.winner = None
        self.game_over = False
        self.moves_count = 0

    def reset_game(self):
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.winner = None
        self.game_over = False
        self.moves_count = 0

    def make_move(self, row, col):
        """Make a move on the board. Return True if move was valid, False otherwise."""
        if self.game_over or row < 0 or row > 2 or col < 0 or col > 2 or self.board[row][col] != '':
            return False
        
        self.board[row][col] = self.current_player
        self.moves_count += 1

        if self.check_winner():
            self.winner = self.current_player
            self.game_over = True
            return True
        
        elif self.moves_count == 9:
            self.game_over = True
            return True
        
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        return True
    
    def check_winner(self):
        """Check if there is a winner. Return True if so, False otherwise."""
        for row in range(3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] != '':
                return True
            
            for col in range(3):
                if self.board[0][col] == self.board[1][col] == self.board[2][col] != '':
                    return True
                
            if self.board[0][0] == self.board[1][1] == self.board[2][2] != '':
                return True
            if self.board[0][2] == self.board[1][1] == self.board[2][0] != '':
                return True
            
            return False
        
    def get_empty_cells(self):
        """Return a list of empty cells as (row, col) tuples."""
        empty_cells = []
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == '':
                    empty_cells.append((row, col))
        return empty_cells
    
    def get_board_state(self):
        """Return a deep copy of the current board state."""
        return [row[:] for row in self.board]