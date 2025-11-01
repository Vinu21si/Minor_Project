# tictactoe_engine.py
# Unbeatable Minimax AI for 3x3 Tic Tac Toe

import math
import copy

def available_moves(board):
    return [i for i, x in enumerate(board) if x == ""]

def check_winner(board):
    wins = [(0,1,2), (3,4,5), (6,7,8),
            (0,3,6), (1,4,7), (2,5,8),
            (0,4,8), (2,4,6)]
    for a, b, c in wins:
        if board[a] != "" and board[a] == board[b] == board[c]:
            return board[a]
    if "" not in board:
        return "draw"
    return None

def minimax(board, player):
    winner = check_winner(board)
    if winner == "X":
        return {"score": -1}
    elif winner == "O":
        return {"score": 1}
    elif winner == "draw":
        return {"score": 0}

    moves = []
    for idx in available_moves(board):
        move = {}
        move["index"] = idx
        board[idx] = player
        if player == "O":
            result = minimax(board, "X")
            move["score"] = result["score"]
        else:
            result = minimax(board, "O")
            move["score"] = result["score"]
        board[idx] = ""
        moves.append(move)

    if player == "O":
        best_score = -math.inf
        best_move = None
        for m in moves:
            if m["score"] > best_score:
                best_score = m["score"]
                best_move = m
        return best_move
    else:
        best_score = math.inf
        best_move = None
        for m in moves:
            if m["score"] < best_score:
                best_score = m["score"]
                best_move = m
        return best_move