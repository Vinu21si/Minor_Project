# chess_engine.py
# Uses python-chess to validate moves and optionally produce engine moves.
import chess
import chess.engine
import os

# Create and manage a Board per session in production; here we expect client to send FEN or moves.
def is_move_legal(fen, uci_move):
    board = chess.Board(fen)
    try:
        move = chess.Move.from_uci(uci_move)
    except:
        return False, "invalid_format"
    return move in board.legal_moves, None

def apply_move(fen, uci_move):
    board = chess.Board(fen)
    move = chess.Move.from_uci(uci_move)
    if move in board.legal_moves:
        board.push(move)
        return board.fen()
    else:
        raise ValueError("Illegal move")

# Optional: get an engine move using a stockfish binary
def engine_move(fen, depth=12, stockfish_path=None):
    board = chess.Board(fen)
    if stockfish_path is None or not os.path.exists(stockfish_path):
        return None
    engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
    try:
        result = engine.play(board, chess.engine.Limit(depth=depth))
        return result.move.uci()
    finally:
        engine.quit()
