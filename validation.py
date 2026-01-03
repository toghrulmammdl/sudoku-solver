def is_valid(board):
    def valid_group(nums):
        nums = [n for n in nums if n != 0]
        return len(nums) == len(set(nums))

    for i in range(9):
        if not valid_group(board[i]): return False
        if not valid_group([board[r][i] for r in range(9)]): return False

    for sr in range(0, 9, 3):
        for sc in range(0, 9, 3):
            box = [
                board[r][c]
                for r in range(sr, sr + 3)
                for c in range(sc, sc + 3)
            ]
            if not valid_group(box): return False

    return True
