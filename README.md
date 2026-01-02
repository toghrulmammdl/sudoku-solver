# 🧩 Sudoku Solver (Logic First, Brute Force Later)

## What This Is

This is a **logic-driven Sudoku solver**.

It applies human-style solving rules (singles, hidden singles, constraint propagation) and only falls back to backtracking **when no logical move remains**.

In short:
- Think first
- Guess only if forced
- Roll back when wrong
- Repeat until the puzzle gives up

---

## What I’ve Built So Far

- A full Sudoku validation system (rows, columns, boxes)
- Candidate-based reasoning for empty cells
- Logical solvers:
  - Naked singles
  - Hidden singles (row / column / box)
- Constraint propagation loop
- Backtracking as a fallback, not the main strategy

The solver is deterministic, rule-respecting, and surprisingly stubborn.

---

## What I Want to Build Next

- **Image-based Sudoku solving**
  - Take a photo or screenshot
  - Read the grid
  - Solve it automatically

- **sudoku.com automation**
  - Read puzzles directly from the website
  - Solve them
  - Auto-fill the solution back into the page  
  *(For educational purposes. Obviously.)*

- More human strategies and a difficulty rating system

---

## About GPT

GPT helped with:
- Writing code faster
- Refactoring
- Acting as a very patient rubber duck

All solving logic and design decisions are mine.  
GPT just typed faster than I do.

---

Built by a developer who got tired of unfinished Sudokus.
