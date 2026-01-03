def print_board(board):
    for row in board:
        print(" ".join(str(n) if n != 0 else "_" for n in row))


def copy_board(board):
    return [row[:] for row in board]


def is_solved(board):
    return all(board[r][c] != 0 for r in range(9) for c in range(9))


def find_first_empty(board):
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                return r, c
    return None
