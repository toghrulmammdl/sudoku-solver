from candidates import candidate_for_cell

def fill_hidden_row(board, row):
    candidates = {
        (row, col): candidate_for_cell(board, row, col)
        for col in range(9)
        if board[row][col] == 0
    }
    return _fill_unique(board, candidates)


def fill_hidden_col(board, col):
    candidates = {
        (row, col): candidate_for_cell(board, row, col)
        for row in range(9)
        if board[row][col] == 0
    }
    return _fill_unique(board, candidates)


def fill_hidden_box(board, sr, sc):
    candidates = {
        (r, c): candidate_for_cell(board, r, c)
        for r in range(sr, sr + 3)
        for c in range(sc, sc + 3)
        if board[r][c] == 0
    }
    return _fill_unique(board, candidates)


def _fill_unique(board, candidates):
    fills = 0
    for num in range(1, 10):
        positions = [pos for pos, cand in candidates.items() if num in cand]
        if len(positions) == 1:
            r, c = positions[0]
            board[r][c] = num
            fills += 1
    return fills
