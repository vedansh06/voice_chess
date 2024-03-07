'''BUGS:
1. Handle evaluations which show mate sequence and run it
2. Download opening book and implement it along with engine
3. Outcome handling:checkmate, check, draw and what type of draw
4. Change depth levels depending on the difficulty level set by user
5. Evaluate in practice.py how many function calls/nodes is done by current algorithm compared to a standard
minimax algorithm
'''

'''if move in opening book:
    play it,
else:
    run engine'''
    


from stockfish import Stockfish
import chess
from math import inf

stockfish = Stockfish(path = r"C:\Users\Vedansh Balasaria\Documents\chess_voice_recognition\stockfish\stockfish-windows-x86-64")
ALPHA = -inf
BETA = inf
engine_board = chess.Board()
    

def minimax(board, depth, max_player, alpha = -inf, beta = inf):
    if board.prev_move is not None:
        engine_board.push_san(board.prev_move)
        board.prev_move = None
        print("thinking...")
    
    if depth == 0 or board.is_in_checkmate("white"):
        stockfish.set_fen_position(engine_board.fen())
        return stockfish.get_evaluation()["value"]
    
    legal_moves = list(str(move) for move in engine_board.legal_moves)
    best_move = None
    if max_player:
        max_eval = -inf
        
        for move in legal_moves:
            engine_board.push_san(move)
            eval = minimax(board, depth-1, False, alpha, beta)
            engine_board.pop()
            
            #breakpoint()
            
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(eval, alpha)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = inf
        for move in legal_moves:

            engine_board.push_san(move)
            eval = minimax(board, depth - 1, True, alpha, beta)
            engine_board.pop()
            
            #breakpoint()
            
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        if depth == 2:
            engine_board.push_san(best_move)
            return best_move
        else:
            return min_eval