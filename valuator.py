import chess

class Valuator:

    MAX_VAL = 100000
    MIN_VAL = -100000

    piece_values =  {chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 0}

    def __init__(self):
        self.memoization = {} # Empty dict for later optimisation, 
                              # key,val = FEN + info, valution.

    # Make object call with state parameter
    def __call__(self, s):
        key = s.key() # To FEN and other info 
        if key not in self.memoization:
            self.memoization[key] = self.value(s)
        
        return self.memoization[key]


    # Value the current state.
    def value(self, s):
        b = s.board

        # Game over values
        if b.is_game_over():
            if b.result() == "1-0": # White wins
                return self.MAX_VAL
            elif b.result() == "0-1": # Black wins
                return self.MIN_VAL
            else:
                return 0 
        
        # Simple valuation: Net piece values
        # Following sign of other chess engines.
        # White is maximising (positive)
        # Black is minimising (negative)

        val = 0.0
        pm = s.board.piece_map()
        for piece in pm:
            piece_val = self.piece_values[pm[piece].piece_type]
            if pm[piece].color == chess.WHITE:
                val += piece_val
            else:
                val -= piece_val

        return val
        




        
    



