import chess

# Wrapper class for chess board (Good for extendability)
class State:
    def __init__(self, fen=None):
        if fen is None:
            self.board = chess.Board()
        else:
            # Careful of shallow copies. Come back later and check docs.
            self.board = chess.Board(fen)

    # Convert state to tuple to be used as caching for memoization.
    def key(self):
        return (self.board.board_fen(), self.board.turn, 
                self.board.castling_rights, self.board.ep_square)

    