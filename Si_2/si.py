import copy

import reversio
from heuristics import *


def minimax(heuristic, board, depth, maximizing_player, visited_nodes):

    visited_nodes[0] += 1

    if depth == 0 or reversio.is_game_over(board):
        return choose_heuristic(heuristic, board), None, visited_nodes[0]

    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        for move in reversio.get_available_moves(board, 'X'):
            new_board = copy.deepcopy(board)
            reversio.make_move(new_board, move[0], move[1], 'X')
            eval, _,  _ = minimax(heuristic, new_board, depth - 1, False, visited_nodes)
            if eval > max_eval:
                max_eval = eval
                best_move = move
        return max_eval, best_move, visited_nodes[0]
    else:
        min_eval = float('inf')
        best_move = None
        for move in reversio.get_available_moves(board, 'O'):
            new_board = copy.deepcopy(board)
            reversio.make_move(new_board, move[0], move[1], 'O')
            eval, _, _ = minimax(heuristic, new_board, depth - 1, True, visited_nodes)
            if eval < min_eval:
                min_eval = eval
                best_move = move
        return min_eval, best_move, visited_nodes[0]

def minimax_alpha_beta(heuristic, board, depth, alpha, beta, maximizing_player, visited_nodes):

    visited_nodes[0] += 1

    if depth == 0 or reversio.is_game_over(board):
        return choose_heuristic(heuristic, board), None, visited_nodes[0]

    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        for move in reversio.get_available_moves(board, 'X'):
            new_board = copy.deepcopy(board)
            reversio.make_move(new_board, move[0], move[1], 'X')
            eval, _, _ = minimax_alpha_beta(heuristic, new_board, depth - 1, alpha, beta, False, visited_nodes)
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Cięcie beta
        return max_eval, best_move, visited_nodes[0]
    else:
        min_eval = float('inf')
        best_move = None
        for move in reversio.get_available_moves(board, 'O'):
            new_board = copy.deepcopy(board)
            reversio.make_move(new_board, move[0], move[1], 'O')
            eval, _, _ = minimax_alpha_beta(heuristic, new_board, depth - 1, alpha, beta, True, visited_nodes)
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break  # Cięcie alfa
        return min_eval, best_move, visited_nodes[0]


def choose_heuristic(heuristic, board):
    if heuristic == 'DEFAULT':
        return evaluate_board(board)
    elif heuristic == 'CORNER':
        return corner_heuristic(board)
    else:
        return combined_heuristic(board,float(heuristic))