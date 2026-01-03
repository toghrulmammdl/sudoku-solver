from puzzles import SUDOKU
from board import print_board
from solver import solve
from propagation import propagate
from validation import is_valid

board = [row[:] for row in SUDOKU]

print("Initial:")
print_board(board)

propagate(board)
solve(board)

print("\nSolved:")
print_board(board)
print("\nValid?", is_valid(board))
