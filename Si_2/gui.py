import pygame
import reversio
import si

CELL_SIZE = 50
BOARD_SIZE = 8

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
YELLOW = (255, 255, 0)


def draw_board(screen, board, available_moves):
    screen.fill(GREEN)
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            x = col * CELL_SIZE
            y = row * CELL_SIZE

            if (row, col) in available_moves:
                pygame.draw.circle(screen, YELLOW, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), 6)

            if board[row][col] == 'X':
                pygame.draw.circle(screen, BLACK, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), CELL_SIZE // 2 - 2)
            elif board[row][col] == 'O':
                pygame.draw.circle(screen, WHITE, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), CELL_SIZE // 2 - 2)

            pygame.draw.rect(screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 1)


def handle_click(board, row, col, current_player):
    if not reversio.is_able_to_move(board,'X'):
        reversio.si_move('CORNER',5,board,'O')
        return
    valid_move = reversio.is_valid_move(board, row, col, current_player)
    if not valid_move:
        print("Nieprawidłowy ruch. Spróbuj ponownie.")
        return

    reversio.make_move(board, row, col, current_player)

    if reversio.is_game_over(board):
        print("Gra zakończona!")
        print(reversio.print_end_game(board))
        #pygame.quit()
        return

    current_player = 'O' if current_player == 'X' else 'X'
    print("Gracz", current_player, " - Twój ruch.")
    heuristic = 'DEFAULT'

    if current_player == 'O':
        reversio.si_move(heuristic, 6, board,'O')


def create_gui() -> object:
    pygame.init()
    screen = pygame.display.set_mode((CELL_SIZE * BOARD_SIZE, CELL_SIZE * BOARD_SIZE))
    pygame.display.set_caption("Reversi")

    board = reversio.create_board()

    current_player = 'X'
    print("Gracz", current_player, " - Twój ruch.")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = x // CELL_SIZE
                row = y // CELL_SIZE
                handle_click(board, row, col, current_player)

        available_moves = reversio.get_available_moves(board, current_player)
        draw_board(screen, board, available_moves)
        pygame.display.update()



