def candidate_for_cell(board, row, col):
    if board[row][col] != 0:
        return []

    used = set(board[row])
    used |= {board[r][col] for r in range(9)}

    sr, sc = 3 * (row // 3), 3 * (col // 3)
    for r in range(sr, sr + 3):
        for c in range(sc, sc + 3):
            used.add(board[r][c])

    return [n for n in range(1, 10) if n not in used]
