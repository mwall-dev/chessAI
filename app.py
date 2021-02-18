import chess
import base64
from flask import Flask, Response, request, render_template, redirect, url_for

from state import State 
from valuator import Valuator 
from treesearch import minimax_root


app = Flask(__name__)


# Instatitate chess board.
s = State()
v = Valuator()
max_depth = 4


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

            computer_move = minimax_root(s, v, max_depth, pruning=True)
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
    
def main():
    app.run(debug=True)




if __name__ == '__main__':
    main()