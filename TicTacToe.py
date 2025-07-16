def display_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 5)

def check_winner(board, player):
    win_conditions = [
        board[0], board[1], board[2],
        [board[i][0] for i in range(3)],
        [board[i][1] for i in range(3)],
        [board[i][2] for i in range(3)],
        [board[i][i] for i in range(3)],
        [board[i][2 - i] for i in range(3)]
    ]
    return [player] * 3 in win_conditions

def tic_tac_toe()
    board