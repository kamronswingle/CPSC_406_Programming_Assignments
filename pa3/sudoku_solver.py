"""PA3 starter: solve Sudoku puzzles using SAT."""

from __future__ import annotations

import ast
import sys

from sat_solver import sat_solve

def varnum(row, col, digit):
    """Encode (row, col, digit) as one positive SAT variable.

    row, col, and digit are all 1-based numbers in {1, ..., 9}.
    """
    return 100 * row + 10 * col + digit


def exactly_one(literals):
    """Return CNF clauses expressing that exactly one literal is true."""
    clauses = [list(literals)]

    # At most one: for every pair, not both can be true.
    for i in range(len(literals)):
        for j in range(i + 1, len(literals)):
            clauses.append([-literals[i], -literals[j]])

    return clauses


def sudoku_encode(grid): # Note, claude did help with this function, it broke down the problem to us and gave us sudocode and how to approach this problem
    clauses = []

    # Each cell contains exactly one digit
    for row in range(1, 10):
        for col in range(1, 10):
            literals = []
            for digit in range(1, 10):
                literals.append(varnum(row, col, digit))
            clauses.extend(exactly_one(literals))

    # Each digit appears exactly once in every row
    for row in range(1, 10):
        for digit in range(1, 10):
            literals = []
            for col in range(1, 10):
                literals.append(varnum(row, col, digit))
            clauses.extend(exactly_one(literals))

    # Each digit appears exactly once in every column
    for col in range(1, 10):
        for digit in range(1, 10):
            literals = []
            for row in range(1, 10):
                literals.append(varnum(row, col, digit))
            clauses.extend(exactly_one(literals))

    # Each digit appears exactly once in every 3x3 box, main thing claude helped with here
    for box_row in range(3):
        for box_col in range(3):
            for digit in range(1, 10):
                literals = []
                for dr in range(1, 4):
                    for dc in range(1, 4):
                        row = 3 * box_row + dr
                        col = 3 * box_col + dc
                        literals.append(varnum(row, col, digit))
                clauses.extend(exactly_one(literals))

    # Fix the given digits
    for row in range(1, 10):
        for col in range(1, 10):
            digit = grid[row - 1][col - 1]
            if digit != 0:
                clauses.append([varnum(row, col, digit)])

    return clauses


def decode_solution(assignment):
    """Convert a satisfying SAT assignment back into a Sudoku grid."""
    grid = [[0 for _ in range(9)] for _ in range(9)]
    for row in range(1, 10):
        for col in range(1, 10):
            for digit in range(1, 10):
                if assignment.get(varnum(row, col, digit)) is True:
                    grid[row - 1][col - 1] = digit
                    break
    return grid


def solve(grid):
    """Return a solved Sudoku grid, or None if the puzzle is unsolvable."""
    clauses = sudoku_encode(grid)
    assignment = sat_solve(clauses, {})
    if assignment is None:
        return None
    return decode_solution(assignment)



def print_result(solution):
    """Print the Sudoku result using the assignment handout format."""
    print(f'solvable: {str(solution is not None).lower()}')
    if solution is None:
        print('solution: None')
        return

    print('solution:')
    for row in solution:
        print(row)


def main():
    """Run the Sudoku solver from the command line on one grid."""
    raw = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    grid = ast.literal_eval(raw)
    print_result(solve(grid))


if __name__ == '__main__':
    main()