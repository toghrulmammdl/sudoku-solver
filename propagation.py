from strategies.naked_single import fill_naked_singles
from strategies.hidden_single import (
    fill_hidden_row, fill_hidden_col, fill_hidden_box
)

def propagate(board):
    while True:
        progress = fill_naked_singles(board)

        for i in range(9):
            progress += fill_hidden_row(board, i)
            progress += fill_hidden_col(board, i)

        for r in range(0, 9, 3):
            for c in range(0, 9, 3):
                progress += fill_hidden_box(board, r, c)

        if progress == 0:
            break
