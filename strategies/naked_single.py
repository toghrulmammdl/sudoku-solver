from candidates import candidate_for_cell

def fill_naked_singles(board):
    fills = 0
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                cand = candidate_for_cell(board, r, c)
                if len(cand) == 1:
                    board[r][c] = cand[0]
                    fills += 1
    return fills
