from board import find_first_empty, copy_board
from candidates import candidate_for_cell
from propagation import propagate

def solve(board):
    pos = find_first_empty(board)
    if pos is None:
        return True

    r, c = pos
    for val in candidate_for_cell(board, r, c):
        snapshot = copy_board(board)
        board[r][c] = val
        propagate(board)
        if solve(board):
            return True
        board[:] = snapshot

    return False
