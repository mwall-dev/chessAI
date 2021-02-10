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


# AI is always black to give human the advantage of development.
def minimax_root(s, v, depth):
    possible_next_moves = list(s.board.legal_moves)
    best_val = v.MAX_VAL
    best_move = None

    for x in possible_next_moves:
        move = chess.Move.from_uci(str(x))
        s.board.push(move)
        value = minimax(s, v, depth - 1)
        s.board.pop()
        if(value <= best_val):
            best_val = value
            best_move = move
        
        print("current move", move)
        print("move_val", value)
        print("best move ", move)
        print()

    print("best val:", best_val)
    return best_move


def minimax(s, v, depth):
    # Stop at a defined maximum depth (chess decision tree too big!) or if game over.
    if(depth == 0  or s.board.is_game_over()):
        return v(s);
    
    turn = s.board.turn;

    # White is the maximising player, black is the minimizing.
    if turn == chess.WHITE:
        max_eval = v.MIN_VAL
        possible_next_moves = list(s.board.legal_moves)

        for move in possible_next_moves:
            s.board.push(move)
            move_eval = minimax(s, v, depth - 1) 
            s.board.pop()

            if move_eval >= max_eval:
                max_eval = move_eval

        return max_eval

    else:
        min_eval = v.MAX_VAL
        possible_next_moves = list(s.board.legal_moves)

        for move in possible_next_moves:
            s.board.push(move)
            move_eval = minimax(s, v, depth - 1) 
            s.board.pop()

            if move_eval <= min_eval:
                min_eval = move_eval

        return min_eval


@app.route('/')
def index():
    return render_template("test-page.html")

@app.route("/move_coordinates")
def move_coordinates():
  if not s.board.is_game_over():
    source = int(request.args.get('from', default=''))
    target = int(request.args.get('to', default=''))

    promotion = True if request.args.get('promotion', default='') == 'true' else False

    move = s.board.san(chess.Move(source, target, promotion=chess.QUEEN if promotion else None))

    if move is not None and move != "":
        print("human moves", move)
        s.board.push_san(move)
        print(s.board.fen())

        computer_move = minimax_root(s, v, 3)
        print("computer moves", computer_move)
        s.board.push(computer_move)

        print(s.board.fen())
    
    response = app.response_class(
      response=s.board.fen(),
      status=200
    )
    return response

  print("GAME IS OVER")
  response = app.response_class(
    response="game over",
    status=200
  )
  return response
    



if __name__ == '__main__':
    app.run(debug=True)