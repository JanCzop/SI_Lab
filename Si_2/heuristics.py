

def evaluate_board(board):
    score = 0
    for row in range(8):
        for col in range(8):
            if board[row][col] == 'X':
                score += 1
            elif board[row][col] == 'O':
                score -= 1
    return score


def corner_heuristic(board):
    corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
    player_scores = {'X': 0, 'O': 0}

    for corner in corners:
        row, col = corner
        if board[row][col] == 'X':
            player_scores['X'] += 1
        elif board[row][col] == 'O':
            player_scores['O'] += 1

    return player_scores['X'] - player_scores['O']


def combined_heuristic(board,N):
    score = N*evaluate_board(board)
    corner = (1-N)*corner_heuristic(board)

    return score + corner
