""" Module containing various tree searching algorithms """

import chess


# Performance statistics
states_visited = 0
leaves_visited = 0


def minimax_root(s, v, depth, pruning=True):
    """ Root function for minimax to handle first call and return best move. """
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
        if(pruning):
            value = minimax(s, v, depth - 1, v.MIN_VAL, v.MAX_VAL)
        else:
            value = minimax_no_pruning(s,v, depth - 1)

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




def minimax(s, v, depth, alpha, beta):
    """ Minimax with alpha-beta pruning. """
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




def minimax_no_pruning(s, v, depth):
    """ Minimax with no pruning to demonstrate efficiency of pruning. """
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
            max_eval = max(minimax_no_pruning(s, v, depth - 1), max_eval) 
            s.board.pop()

        return max_eval

    else:
        min_eval = v.MAX_VAL - 1
        possible_next_moves = list(s.board.legal_moves)

        for move in possible_next_moves:
            s.board.push(move)
            min_eval = min(minimax_no_pruning(s, v, depth - 1), min_eval) 
            s.board.pop()

        return min_eval
