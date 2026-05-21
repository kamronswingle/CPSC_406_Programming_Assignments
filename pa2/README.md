# PA2: General SAT Solver

  ## Collaborators
  - Kamron Swingle
  - Jun Yi
  - Taylor Eskew

  ## Overview
  This program determines whether a propositional formula in **conjunctive normal form (CNF)** is satisfiable, and returns a satisfying assignment
  when one exists. It generalizes PA1 from Horn formulas to arbitrary CNF using the **DPLL algorithm**: a recursive search that combines
  simplification, unit propagation, and case-splitting on unassigned variables.

  ## How It Works

  Each clause is a list of integer literals — positive for a variable, negative for its negation:
  - `[1]` → unit clause: `x₁` must be true
  - `[-2]` → unit clause: `x₂` must be false
  - `[1, -2, 3]` → clause: `x₁ ∨ ¬x₂ ∨ x₃`

  The solver:
  1. **Simplifies** the formula under the current partial assignment — drops satisfied clauses, removes falsified literals from the rest, and reports
   a contradiction if any clause becomes empty
  2. **Unit propagates** — repeatedly forces the assignment implied by any clause that has shrunk to a single literal, re-simplifying after each
  forced assignment
  3. **Detects base cases** — if simplification fails, the branch is unsatisfiable; if no clauses remain, the assignment is satisfying
  4. **Branches** on an unassigned variable, recursively trying `True` and then `False`, copying the assignment so failed branches do not contaminate
   sibling branches

  ## Usage

  ```bash
  python3 sat_solver.py "[[1, 2], [-1, 2], [1, -2]]"

  Output

  satisfiable: true
  assignment: {1: True, 2: True}

  Unsatisfiable formulas print satisfiable: false and assignment: None.

  Running Tests

  From the pa2 directory:

  python3 tests/test_pa2.py --solution sat_solver.py
