import chess
import base64
import traceback
from flask import Flask, Response, request, render_template, redirect, url_for

from state import State 
from valuator import Valuator 



app = Flask(__name__)


# Instatitate chess board.
s = State()
v = Valuator()


def minimax(s, v, depth):
    # Stop at a defined maximum depth (chess decision tree too big!) or if game over.
    if(depth == 0  or s.board.is_game_over()):
        return s.board.peek(), v(s);
    
    turn = s.board.turn;

    # White is the maximising player, black is the minimizing.
    if turn == chess.WHITE:
        max_eval = v.MIN_VAL
        possible_next_moves = list(s.board.legal_moves)

        for move in possible_next_moves:
            s.board.push(move)
            new_move, move_eval = minimax(s, v, depth - 1) 
            s.board.pop()

            if move_eval > max_eval:
                max_eval = move_eval
                best_move = new_move

        return best_move, max_eval

    else:
        min_eval = v.MAX_VAL
        possible_next_moves = list(s.board.legal_moves)

        for move in possible_next_moves:
            print(move)
            s.board.push(move)
            new_move, move_eval = minimax(s, v, depth - 1) 
            s.board.pop()
            if move_eval < min_eval:
                min_eval = move_eval
                best_move = new_move

        return best_move, min_eval


@app.route('/')
def index():
    return render_template("test-page.html")





if __name__ == '__main__':
    app.run(debug=True)