import chess

class Valuator:

    MAX_VAL = 100000
    MIN_VAL = -100000

    piece_values =  {chess.PAWN: 10,
            chess.KNIGHT: 30,
            chess.BISHOP: 30,
            chess.ROOK: 50,
            chess.QUEEN: 90,
            chess.KING: 900}


    # Postional values. Use [-square_num] for black.
    position_values = {
            chess.PAWN: [
                0, 0, 0, 0, 0, 0, 0, 0,
                5, 5, 5, 5, 5, 5, 5, 5,
                1, 1, 2, 3, 3, 2, 1, 1,
                0.5, 0.5, 1, 2.5, 2.5, 1, 0.5, 0.5,
                0, 0, 0, 2, 2, 0, 0, 0,
                0.5, -0.5, -1, 0, 0, -1, -0.5, 0.5,
                0.5, 1, 1, -2, -2, 1, 1, 0.5,
                0, 0, 0, 0, 0, 0, 0, 0
            ],
            chess.KNIGHT: [
                -5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0,
                -4.0, -2.0,  0.0,  0.0,  0.0,  0.0, -2.0, -4.0,
                -3.0,  0.0,  1.0,  1.5,  1.5,  1.0,  0.0, -3.0,
                -3.0,  0.5,  1.5,  2.0,  2.0,  1.5,  0.5, -3.0,
                -3.0,  0.0,  1.5,  2.0,  2.0,  1.5,  0.0, -3.0,
                -3.0,  0.5,  1.0,  1.5,  1.5,  1.0,  0.5, -3.0,
                -4.0, -2.0,  0.0,  0.5,  0.5,  0.0, -2.0, -4.0,
                -5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0
            ],
            chess.BISHOP: [
                -2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0,
                -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0,
                -1.0,  0.0,  0.5,  1.0,  1.0,  0.5,  0.0, -1.0,
                -1.0,  0.5,  0.5,  1.0,  1.0,  0.5,  0.5, -1.0,
                -1.0,  0.0,  1.0,  1.0,  1.0,  1.0,  0.0, -1.0,
                -1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0, -1.0,
                -1.0,  0.5,  0.0,  0.0,  0.0,  0.0,  0.5, -1.0,
                -2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0
            ],
            chess.ROOK: [
                0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,
                0.5,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  0.5,
                -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5,
                -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5,
                -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5,
                -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5,
                -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5,
                0.0,  0.0, 0.0,  0.5,  0.5,  0.0,  0.0,  0.0
            ],
            chess.QUEEN: [
                 -2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0,
                 -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0,
                 -1.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0,
                 -0.5,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5,
                  0.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5,
                 -1.0,  0.5,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0,
                 -1.0,  0.0,  0.5,  0.0,  0.0,  0.0,  0.0, -1.0,
                 -2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0
            ],
            chess.KING: [
                 -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0,
                 -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0,
                 -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0,
                 -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0,
                 -2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0,
                 -1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0,
                  2.0,  2.0,  0.0,  0.0,  0.0,  0.0,  2.0,  2.0,
                  2.0,  3.0,  1.0,  0.0,  0.0,  1.0,  3.0,  2.0
            ]
        }

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
        
        # Net piece values & positional values
        # Following sign of other chess engines.
        # White is maximising (positive)
        # Black is minimising (negative)
        val = 0.0
        pm = s.board.piece_map()

        for square, piece in pm.items():
            # Get piece value
            piece_val = self.piece_values[piece.piece_type]

            if piece.color == chess.WHITE:
                val += piece_val
                val += self.position_values[piece.piece_type][square]
            else:
                val -= piece_val
                val -= self.position_values[piece.piece_type][-square]


        return val
        




        
    



