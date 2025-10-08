# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, User, Score
from tictactoe_engine import minimax, check_winner
from chess_engine import is_move_legal, apply_move, engine_move
import os

app = Flask(__name__)
CORS(app)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

# Simple auth/register
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    if not username:
        return jsonify({"error":"username required"}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({"error":"exists"}), 409
    u = User(username=username)
    db.session.add(u); db.session.commit()
    return jsonify({"ok":True, "username":username})

# Leaderboard
@app.route('/scores', methods=['GET'])
def get_scores():
    # aggregate
    t_wins = Score.query.filter_by(game='tictactoe', result='win').count()
    chess_moves = Score.query.filter_by(game='chess', result='move').count()
    return jsonify({"tictactoe_wins": t_wins, "chess_moves": chess_moves})

# TicTacToe move: client sends board, AI plays O (server returns ai_move index)
@app.route('/tictactoe/ai_move', methods=['POST'])
def ttt_ai_move():
    data = request.json
    board = data.get('board')  # list of 9: "", "X", "O"
    if not board or len(board)!=9:
        return jsonify({"error":"bad_board"}),400
    # AI is O (maximizer). If game already finished return status
    winner = check_winner(board)
    if winner:
        return jsonify({"winner": winner})
    move = minimax(board.copy(), "O")
    if move is None:
        return jsonify({"winner": "draw"})
    ai_index = move["index"]
    return jsonify({"ai_index": ai_index})

# Chess endpoints
@app.route('/chess/validate_move', methods=['POST'])
def chess_validate():
    data = request.json
    fen = data.get('fen')
    uci = data.get('move')
    ok, reason = is_move_legal(fen, uci)
    return jsonify({"legal": ok, "reason": reason})

@app.route('/chess/apply_move', methods=['POST'])
def chess_apply():
    data = request.json
    fen = data.get('fen')
    uci = data.get('move')
    try:
        newfen = apply_move(fen, uci)
        return jsonify({"fen": newfen})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Optional engine move (requires stockfish installed and path provided)
@app.route('/chess/engine_move', methods=['POST'])
def chess_engine_move():
    data = request.json
    fen = data.get('fen')
    sf_path = data.get('stockfish_path')
    mv = engine_move(fen, stockfish_path=sf_path)
    if mv is None:
        return jsonify({"error":"engine not available"}), 400
    return jsonify({"uci": mv})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
