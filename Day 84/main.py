# Tic Tac Toe game in Python - Command Line Version
# Human vs AI opponent (Human plays X, AI plays O)


def create_board():
    """Create and return a 3x3 Tic Tac Toe board initialized with spaces."""
    return [[" " for _ in range(3)] for _ in range(3)]


def display_board(board):
    """Display the Tic Tac Toe board in the command line."""
    print("   1   2   3")
    for i, row in enumerate(board):
        print(f"{i+1}  " + " | ".join(row))
        if i < 2:
            print("  ---+---+---")


def check_win(board, player):
    """Check if the given player has won the game."""
    # Check rows and columns
    for i in range(3):
        if all(cell == player for cell in board[i]):
            return True
        if all(board[r][i] == player for r in range(3)):
            return True

    # Check diagonals
    if all(board[i][i] == player for i in range(3)):
        return True
    if all(board[i][2-i] == player for i in range(3)):
        return True

    return False


def check_tie(board):
    """Check if the game is a tie (board full with no winner)."""
    return all(cell != " " for row in board for cell in row)


def get_player_move(board, player):
    """Prompt the human player to enter a valid move and return the (row, col) indices."""
    while True:
        move = input(f"Player {player}, enter your move as row and column (e.g. '1 3'): ")
        parts = move.split()
        if len(parts) != 2:
            print("Invalid input format. Please enter two numbers separated by a space.")
            continue
        try:
            row, col = int(parts[0]), int(parts[1])
        except ValueError:
            print("Invalid input. Please enter numeric values.")
            continue
        if not (1 <= row <= 3 and 1 <= col <= 3):
            print("Invalid input. Row and column must be between 1 and 3.")
            continue
        if board[row-1][col-1] != " ":
            print("That cell is already occupied. Try again.")
            continue
        return row-1, col-1


def minimax(board, player):
    """Minimax algorithm to choose the best move for AI (O) or simulate opponent (X)."""
    # Base cases
    if check_win(board, 'O'):
        return 1, None         # AI wins
    if check_win(board, 'X'):
        return -1, None        # Human wins
    if check_tie(board):
        return 0, None         # Tie

    moves = []
    for r in range(3):
        for c in range(3):
            if board[r][c] == " ":
                board[r][c] = player
                score, _ = minimax(board, 'X' if player == 'O' else 'O')
                moves.append((score, (r, c)))
                board[r][c] = " "

    # Choose the best move
    if player == 'O':  # AI's turn, maximize score
        best = max(moves, key=lambda x: x[0])
    else:               # Human's turn, minimize AI score
        best = min(moves, key=lambda x: x[0])
    return best


def get_ai_move(board):
    """Determine the AI's move using minimax and return the (row, col) indices."""
    _, move = minimax(board, 'O')
    return move


def tic_tac_toe():
    """Main function to run the Tic Tac Toe game loop with optional AI opponent."""
    # Choose game mode
    mode = input("Do you want to play against the AI? (y/n): ").strip().lower()
    ai_enabled = (mode == 'y')

    while True:
        board = create_board()
        current_player = 'X'
        game_over = False

        while not game_over:
            display_board(board)
            if current_player == 'X' or not ai_enabled:
                # Human move
                row, col = get_player_move(board, current_player)
            else:
                # AI move
                print("AI is making a move...")
                row, col = get_ai_move(board)

            board[row][col] = current_player

            # Check for win or tie
            if check_win(board, current_player):
                display_board(board)
                winner = "AI (O)" if (current_player == 'O' and ai_enabled) else f"Player {current_player}"
                print(f"Congratulations! {winner} wins!")
                game_over = True
            elif check_tie(board):
                display_board(board)
                print("The game is a tie!")
                game_over = True
            else:
                # Switch player
                current_player = 'O' if current_player == 'X' else 'X'

        # Ask if players want to play again
        play_again = input("Do you want to play again? (y/n): ").strip().lower()
        if play_again != 'y':
            print("Thanks for playing Tic Tac Toe!")
            break


if __name__ == "__main__":
    tic_tac_toe()
