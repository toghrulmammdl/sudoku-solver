SUDOKU  = [
    [3, 0, 0, 0, 4, 0, 9, 6, 0],
    [9, 0, 0, 0, 0, 8, 0, 1, 0],
    [6, 0, 0, 0, 0, 5, 0, 0, 0],

    [0, 0, 8, 0, 0, 4, 0, 9, 0],
    [1, 0, 0, 3, 0, 0, 0, 2, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],

    [0, 0, 0, 0, 0, 0, 5, 0, 6],
    [0, 0, 1, 0, 5, 0, 0, 0, 2],
    [0, 0, 7, 0, 0, 2, 0, 4, 0],
]

def print_sudoku(board):
    for row in board:
        for num in row:
            print(num if num != 0 else '_', end=' ')
        print()

def is_valid(board):
    def is_valid_row(row):
        nums = [num for num in board[row] if num != 0]
        if len(nums) != len(set(nums)):
            print("Invalid row")
            return False
        return True
    
    def is_valid_column(col):
        column = [board[num][col] for num in range(9)]
        nums = [num for num in column if num != 0]
        if len(nums) != len(set(nums)):
            print("Invalid col")
            return False
        return True
    
    def is_valid_subgrid(start_row, start_col):
        nums = []
        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):
                if board[r][c] != 0:
                    nums.append(board[r][c])
        if len(nums) != len(set(nums)):
            print("Invalid subgrid")
            return False
        return True
    
    for row in range(9):
        if not is_valid_row(row):
            return False
    for col in range(9):
        if not is_valid_column(col):
            return False
    for row in range(0, 9, 3):
        for col in range(0, 9, 3):
            if not is_valid_subgrid(row, col):
                return False
    return True

def candidate_for_cell(board, row, col):
    if board[row][col] != 0:
        return []

    used_numbers = set()

    for num in board[row]:
        if num != 0:
            used_numbers.add(num)

    for r in range(9):
        num = board[r][col]
        if num != 0:
            used_numbers.add(num)

    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            num = board[r][c]
            if num != 0:
                used_numbers.add(num)

    candidates = [num for num in range(1, 10) if num not in used_numbers]
    return candidates

def fill_single_candidates_once(board):
    fills = 0
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                cand = candidate_for_cell(board, row, col)
                if len(cand) == 1:
                    board[row][col] = cand[0]
                    fills += 1
    return fills

def repeat_fill_single_candidates(board):
    total = 0
    while True:
        filled = fill_single_candidates_once(board)
        if filled == 0:
            break
        total += filled
    return total

def fill_hidden_single_in_row(board, row):
    row_candidates = [[] for _ in range(9)]
    for col in range(9):
        if board[row][col] == 0:
            row_candidates[col] = candidate_for_cell(board, row, col)

    fills = 0
    for number in range(1, 10):
        positions = [col for col in range(9) if number in row_candidates[col]]
        if len(positions) == 1:
            col = positions[0]
            board[row][col] = number
            fills += 1
    return fills

def fill_hidden_single_in_column(board, col):
    col_candidates = [[] for _ in range(9)]
    for row in range(9):
        if board[row][col] == 0:
            col_candidates[row] = candidate_for_cell(board, row, col)

    fills = 0
    for number in range(1, 10):
        positions = [row for row in range(9) if number in col_candidates[row]]
        if len(positions) == 1:
            row = positions[0]
            board[row][col] = number
            fills += 1
    return fills

def fill_hidden_single_in_subgrid(board, start_row, start_col):
    cells = []
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            cells.append((r, c))

    candidates = {}
    for (r, c) in cells:
        if board[r][c] == 0:
            candidates[(r, c)] = candidate_for_cell(board, r, c)

    fills = 0
    for number in range(1, 10):
        positions = [(r, c) for (r, c), cand in candidates.items() if number in cand]
        if len(positions) == 1:
            r, c = positions[0]
            board[r][c] = number
            fills += 1
    return fills

def fill_hidden_singles(board):
    total = 0
    for row in range(9):
        total += fill_hidden_single_in_row(board, row)
    for col in range(9):
        total += fill_hidden_single_in_column(board, col)
    for row in range(0, 9, 3):
        for col in range(0, 9, 3):
            total += fill_hidden_single_in_subgrid(board, row, col)
    return total

def repeat_fill_hidden_singles(board):
    total = 0
    while True:
        filled = fill_hidden_singles(board)
        if filled == 0:
            break
        total += filled
    return total

def propagate_all(board):
    steps = 0
    while True:
        filled1 = repeat_fill_single_candidates(board)
        filled2 = repeat_fill_hidden_singles(board)

        if filled1 == 0 and filled2 == 0:
            break
        steps += 1
    return steps

def is_solved(board):
    return all(board[r][c] != 0 for r in range(9) for c in range(9))

def find_first_empty(board):
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                return r, c
    return None

def solve(board):
    empty = find_first_empty(board)
    if empty is None:
        return True

    r, c = empty
    cands = candidate_for_cell(board, r, c)
    if len(cands) == 0:
        return False

    for val in cands:
        snapshot = [row[:] for row in board]
        board[r][c] = val
        propagate_all(board)
        if solve(board): return True
        board[:] = snapshot

    return False

if __name__ == "__main__":
    
    print("Initial Sudoku:")
    board = [row[:] for row in SUDOKU]
    print("\nInitial Sudoku:")
    print_sudoku(board)
    propagate_all(board)
    print("\nAfter propagation:")
    print_sudoku(board)
    ok = solve(board)
    print("\nSolved Sudoku:")
    print_sudoku(board)
    print("\nIs the Sudoku solved?", ok)
    print("\nSolved Sudoku:")
    print("\nValid?", is_valid(board))
