import pygame
import sys

# Initialize Pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (70, 130, 180)
RED = (220, 20, 60)

# Screen settings
SCREEN_SIZE = 600
FPS = 60
font = pygame.font.Font(None, 48)

def draw_grid(screen, size):
    """Draws the grid based on the board size."""
    block_size = SCREEN_SIZE // size
    for i in range(1, size):
        pygame.draw.line(screen, BLACK, (block_size * i, 0), (block_size * i, SCREEN_SIZE), 2)
        pygame.draw.line(screen, BLACK, (0, block_size * i), (SCREEN_SIZE, block_size * i), 2)

def draw_board(screen, board, size):
    """Draws the current state of the board."""
    block_size = SCREEN_SIZE // size
    for i in range(size):
        for j in range(size):
            symbol = board[i][j]
            if symbol != " ":
                text = font.render(symbol, True, BLUE if symbol == "X" else RED)
                x = j * block_size + block_size // 2 - text.get_width() // 2
                y = i * block_size + block_size // 2 - text.get_height() // 2
                screen.blit(text, (x, y))

def check_winner(board, player, size):
    """Check if a player has won."""
    # Check rows and columns
    for i in range(size):
        if all(board[i][j] == player for j in range(size)) or all(board[j][i] == player for j in range(size)):
            return True
    # Check diagonals
    return all(board[i][i] == player for i in range(size)) or all(board[i][size - 1 - i] == player for i in range(size))

def get_available_moves(board):
    """Returns a list of available moves."""
    return [(i, j) for i in range(len(board)) for j in range(len(board)) if board[i][j] == " "]

def is_full(board):
    """Checks if the board is full."""
    return all(cell != " " for row in board for cell in row)

def minimax(board, depth, is_maximizing, alpha, beta, size):
    """Minimax algorithm with alpha-beta pruning."""
    if check_winner(board, "O", size):
        return 10 - depth
    if check_winner(board, "X", size):
        return depth - 10
    if is_full(board):
        return 0

    if is_maximizing:
        max_eval = float('-inf')
        for i, j in get_available_moves(board):
            board[i][j] = "O"
            eval = minimax(board, depth + 1, False, alpha, beta, size)
            board[i][j] = " "
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for i, j in get_available_moves(board):
            board[i][j] = "X"
            eval = minimax(board, depth + 1, True, alpha, beta, size)
            board[i][j] = " "
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def best_move(board, size):
    """Finds the best move for AI."""
    best_score = float('-inf')
    move = None
    for i, j in get_available_moves(board):
        board[i][j] = "O"
        score = minimax(board, 0, False, float('-inf'), float('inf'), size)
        board[i][j] = " "
        if score > best_score:
            best_score = score
            move = (i, j)
    return move

def main():
    # Customizations
    size = int(input("Enter board size (e.g., 3 for 3x3): "))
    player_symbol = input("Choose your symbol (X or O): ").upper()
    ai_symbol = "O" if player_symbol == "X" else "X"

    # Initialize board
    board = [[" " for _ in range(size)] for _ in range(size)]

    # Pygame setup
    screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
    pygame.display.set_caption("Tic Tac Toe")
    clock = pygame.time.Clock()

    running = True
    player_turn = True

    while running:
        screen.fill(WHITE)
        draw_grid(screen, size)
        draw_board(screen, board, size)
        pygame.display.flip()

        if check_winner(board, player_symbol, size):
            print("You win!")
            running = False
        elif check_winner(board, ai_symbol, size):
            print("AI wins!")
            running = False
        elif is_full(board):
            print("It's a tie!")
            running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if player_turn and event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                row, col = y // (SCREEN_SIZE // size), x // (SCREEN_SIZE // size)
                if board[row][col] == " ":
                    board[row][col] = player_symbol
                    player_turn = False

        if not player_turn:
            ai_move = best_move(board, size)
            if ai_move:
                board[ai_move[0]][ai_move[1]] = ai_symbol
            player_turn = True

        clock.tick(FPS)

if __name__ == "__main__":
    main()
