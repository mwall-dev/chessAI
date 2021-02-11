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
    global states_visited
    global leaves_visited
    leaves_visited = 0
    states_visited = 0
    v.cache_misses = 0

    possible_next_moves = list(s.board.legal_moves)
    best_val = v.MAX_VAL
    best_move = None

    for x in possible_next_moves:
        move = chess.Move.from_uci(str(x))
        s.board.push(move)
        value = minimax(s, v, depth - 1, v.MIN_VAL, v.MAX_VAL)
        s.board.pop()
        if(value <= best_val):
            best_val = value
            best_move = move
        
        #print("current move", move)
        #print("move_val", value)
        #print("best move ", move)
        #print("-------------")
    print("-----------------------")
    print("Info")
    print("-----------------------")
    print("States visited:", states_visited) 
    print("leaves visited:", leaves_visited)
    print("cache hits:",leaves_visited - v.cache_misses)
    print("Best computer move:", best_move)
    print("best val:", best_val)
    print("------------------------")
    return best_move


states_visited = 0
leaves_visited = 0
def minimax(s, v, depth, alpha, beta):
    global states_visited
    global leaves_visited
    states_visited+=1
    # Stop at a defined maximum depth (chess decision tree too big!) or if game over.
    if(depth == 0  or s.board.is_game_over()):
        leaves_visited += 1
        return v(s);
    
    turn = s.board.turn;

    # White is the maximising player, black is the minimizing.
    if turn == chess.WHITE:
        max_eval = v.MIN_VAL + 1
        possible_next_moves = list(s.board.legal_moves)

        for move in possible_next_moves:
            s.board.push(move)
            max_eval = max(minimax(s, v, depth - 1, alpha, beta), max_eval) 
            s.board.pop()
            alpha = max(alpha, max_eval)
            if beta <= alpha:
                return max_eval

        return max_eval

    else:
        min_eval = v.MAX_VAL - 1
        possible_next_moves = list(s.board.legal_moves)

        for move in possible_next_moves:
            s.board.push(move)
            min_eval = min(minimax(s, v, depth - 1, alpha, beta), min_eval) 
            s.board.pop()
            beta = min(beta, min_eval)
            if beta <= alpha:
                return min_eval

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
        print("Human moves", move)
        print("Computing... ")
        s.board.push_san(move)
        #print(s.board.fen())

        computer_move = minimax_root(s, v, 4)
        #print("computer moves", computer_move)
        s.board.push(computer_move)

        #print(s.board.fen())
    
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