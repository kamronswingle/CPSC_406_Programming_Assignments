# PA3: Sudoku SAT Solver

## Collaborators

- Kamron Swingle
- Jun Yi
- Taylor Eskew

## Overview
This program solves 9x9 Sudoku puzzles by reducing them to a **SAT problem** and solving it
using the DPLL-based SAT solver from PA2. The puzzle is encoded into CNF clauses that capture
all Sudoku rules, and the satisfying assignment is decoded back into a solved grid.

## How It Works

**Encoding**
Each possible (row, col, digit) combination is represented as a unique SAT variable via `varnum`.
For example, `varnum(3, 5, 7)` represents "cell (3,5) contains the digit 7". The encoder adds
clauses enforcing four Sudoku rules:

1. Every cell contains exactly one digit
2. Every digit appears exactly once in each row
3. Every digit appears exactly once in each column
4. Every digit appears exactly once in each 3x3 box

Given digits from the puzzle are added as unit clauses, which immediately trigger unit propagation
in the SAT solver.

**Decoding**
Once the SAT solver returns a satisfying assignment, the decoder reads which `varnum(row, col, digit)`
variables are `True` and reconstructs the solved grid.

## Usage
```bash
python3 sudoku_solver.py "[[5,3,0,0,7,0,0,0,0], ...]"
```

## Output