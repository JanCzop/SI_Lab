import si


def create_board():
    board = [[' ' for _ in range(8)] for _ in range(8)]
    board[3][3] = 'O'
    board[3][4] = 'X'
    board[4][3] = 'X'
    board[4][4] = 'O'
    return board

# Wyświetlanie planszy
def print_board(board):
    print('  0 1 2 3 4 5 6 7')
    print(' -----------------')
    for row in range(8):
        print(row, end='|')
        for col in range(8):
            print(board[row][col], end=' ')
        print('|')
    print(' -----------------')

def is_valid_coordinate(row, col):
    return 0 <= row < 8 and 0 <= col < 8

def is_valid_move(board, row, col, player):
    if not is_valid_coordinate(row, col) or board[row][col] != ' ':
        return False
    other_player = 'O' if player == 'X' else 'X'
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    for dx, dy in directions:
        x, y = row + dx, col + dy
        if is_valid_coordinate(x, y) and board[x][y] == other_player:
            x += dx
            y += dy
            while is_valid_coordinate(x, y) and board[x][y] == other_player:
                x += dx
                y += dy
            if is_valid_coordinate(x, y) and board[x][y] == player:
                return True
    return False


def count_points(board):
    x_score = 0
    o_score = 0
    for row in board:
        x_score += row.count('X')
        o_score += row.count('O')
    return x_score, o_score


def is_game_over(board):
    x_count, o_count = count_points(board)
    if x_count == 0 or o_count == 0:
        return True

    for row in board:
        if ' ' in row:
            return False
    return True

def is_able_to_move(board, player):
        return not get_available_moves(board,player) == []

def get_available_moves(board, player):
    available_moves = []
    for row in range(8):
        for col in range(8):
            if is_valid_move(board, row, col, player):
                available_moves.append((row, col))
    return available_moves

def print_end_game(board):
    #print('\n')
    #print_board(board)
    x_score, o_score = count_points(board)
    print("Gra zakończona.")
    print("Wynik:")
    print("Gracz X:", x_score)
    print("Gracz O:", o_score)
    if o_score>x_score:
        print("Gracz Czarny wygrał")
    else:
        print("Gracz Biały wygrał")

def return_results(board, x_nodes_number, o_nodes_number):
    return count_points(board),x_nodes_number,o_nodes_number


def make_move(board, row, col, player):
    if not is_valid_move(board, row, col, player):
        return False

    other_player = 'O' if player == 'X' else 'X'
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    board[row][col] = player

    for dx, dy in directions:
        x, y = row + dx, col + dy
        tokens_to_flip = []

        while is_valid_coordinate(x, y) and board[x][y] == other_player:
            tokens_to_flip.append((x, y))
            x += dx
            y += dy

        if is_valid_coordinate(x, y) and board[x][y] == player:
            flip_tokens(board, tokens_to_flip, player)

    return True


def flip_tokens(board, tokens, player):
    for row, col in tokens:
        board[row][col] = player


def start_game_player_vs_player():
    board = create_board()
    current_player = 'X'
    game_over = False

    while not game_over:
        print_board(board)
        print("Gracz", current_player, " - Twój ruch.")

        available_moves = get_available_moves(board, current_player)
        print("Dostępne ruchy:", available_moves)

        valid_move = False
        while not valid_move:
            try:
                row = int(input("Podaj numer wiersza (0-7): "))
                col = int(input("Podaj numer kolumny (0-7): "))
                valid_move = is_valid_move(board, row, col, current_player)
                if not valid_move:
                    print("Nieprawidłowy ruch. Spróbuj ponownie.")
            except ValueError:
                print("Nieprawidłowe współrzędne. Spróbuj ponownie.")

        make_move(board, row, col, current_player)

        current_player = 'O' if current_player == 'X' else 'X'

        if is_game_over(board):
            game_over = True

    print_end_game(board)




def start_game_player_vs_si():
    board = create_board()
    current_player = 'X'
    game_over = False

    while not game_over:
        print_board(board)

        if current_player == 'X':
            players_move(board,current_player)
        else:
            si_move(board,6 ,current_player)

        current_player = 'O' if current_player == 'X' else 'X'
        if is_game_over(board):
            game_over = True

    print_end_game(board)



def start_game_si_vs_si(SI_1,SI_2):
    board = create_board()
    current_player = 'X'
    player_x_nodes = 0
    player_o_nodes = 0

    while not is_game_over(board):
        if current_player == 'X':
            player_x_nodes += si_move_returning(SI_1[0], SI_1[1], board,SI_1[2],SI_1[3],'X',SI_1[4])
        else:
            player_o_nodes += si_move_returning(SI_2[0], SI_2[1], board, SI_2[2], SI_2[3], 'O', SI_2[4])
   #     print_board(board)
        current_player = 'O' if current_player == 'X' else 'X'
    print_end_game(board)
    print('Odwiedzona ilosc węzłów gracza X',player_x_nodes)
    print('Odwiedzona ilosc węzłów gracza O',player_o_nodes)
    return return_results(board,player_x_nodes,player_o_nodes)









def players_move(board, current_player):
    print("Gracz", current_player, "- Twój ruch.")
    available_moves = get_available_moves(board, current_player)
    print("Dostępne ruchy:", available_moves)

    valid_move = False
    while not valid_move:
        try:
            row = int(input("Podaj numer wiersza (0-7): "))
            col = int(input("Podaj numer kolumny (0-7): "))
            valid_move = is_valid_move(board, row, col, current_player)
            if not valid_move:
                print("Nieprawidłowy ruch. Spróbuj ponownie.")
        except ValueError:
            print("Nieprawidłowe współrzędne. Spróbuj ponownie.")
    make_move(board, row, col, current_player)

def si_move(heuristic, depth, board,current_player):
    print("Ruch SI (Gracz", current_player + ")")
    available_moves = get_available_moves(board, current_player)
    print("Dostępne ruchy:", available_moves)
    player_flag = False if current_player == 'O' else True
    best_score, best_move, visited_nodes = si.minimax_alpha_beta(heuristic,board, depth, float('-inf'), float('inf'), player_flag, [0])
    print('przeszukane węzły: ',{visited_nodes})
    print('najlepszy  ruch SI:')
    print(best_move)
    if best_move is not None:
        make_move(board, best_move[0], best_move[1], current_player)


def choose_algorithm(heuristic,board,depth,alfa,beta,player_flag,algorithm):
    if  algorithm == 'DEF':
        return si.minimax(heuristic,board,depth,player_flag,[0])
    elif  algorithm == 'AB':
        return si.minimax_alpha_beta(heuristic,board,depth,alfa,beta,player_flag,[0])

def si_move_returning(heuristic, depth, board,alfa,beta,current_player, algorithm):
    player_flag = False if current_player == 'O' else True
    best_score, best_move, visited_nodes = choose_algorithm(heuristic,board,depth,alfa,beta,player_flag,algorithm)
  #  print('przeszukane węzły: ',{visited_nodes})
  #  print('ruch SI:')
  #  print(best_move)
    if best_move is not None:
        make_move(board, best_move[0], best_move[1], current_player)
    return visited_nodes