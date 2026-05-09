"""Same SAT Solver from pa2, reused here, same functionality
"""

from __future__ import annotations

import ast
import sys


def literal_variable(literal):
    """Return the variable number appearing in a literal."""
    return abs(literal)


def literal_required_value(literal):
    """Return the value that makes a literal true."""
    return literal > 0


def evaluate_literal(literal, assignment):
    """Evaluate one literal under a partial assignment.

    Return:
      True if the literal is already true,
      False if the literal is already false,
      None if its variable is not assigned yet.
    """
    variable = literal_variable(literal)
    if variable not in assignment:
        return None
    return assignment[variable] == literal_required_value(literal)


def simplify(clauses, assignment):
    """Simplify clauses under a partial assignment.

    Clauses that are already true disappear. Literals that are already false are
    removed from their clauses. If a clause becomes empty, the current partial
    assignment cannot lead to a solution.
    """
    simplified = []
    for clause in clauses:
        new_clause = []
        clause_satisfied = False

        for literal in clause:
            value = evaluate_literal(literal, assignment)
            if value is True:
                clause_satisfied = True
                break
            if value is None:
                new_clause.append(literal)

        if clause_satisfied:
            continue
        if len(new_clause) == 0:
            return None
        simplified.append(new_clause)

    return simplified


def unit_propagate(clauses, assignment):
    """Repeatedly apply unit clauses.

    This is one of the key algorithmic parts of the assignment.
    """
    simplified = simplify(clauses, assignment)
    if simplified is None:
        return None
    while True:
        unit_literal = None
        for clause in simplified:
            if len(clause) == 1:
                unit_literal = clause[0]
                break
        if unit_literal is None:
            return simplified
        
        assignment[literal_variable(unit_literal)] = literal_required_value(unit_literal)
        simplified = simplify(simplified, assignment)
        if simplified is None:
            return None


def choose_variable(clauses, assignment):
    """Choose an unassigned variable to branch on.

    This simple helper returns the first unassigned variable it sees. You may
    replace it by a smarter heuristic.
    """
    for clause in clauses:
        for literal in clause:
            variable = literal_variable(literal)
            if variable not in assignment:
                return variable
    return None


def sat_solve(clauses, assignment):
    """Solve SAT for a CNF formula by extending the given partial assignment.

    Return a satisfying assignment if one exists. Return None otherwise.
    """
    assignment = dict(assignment)

    simplified = unit_propagate(clauses, assignment)
    if simplified is None:
        return None
    if len(simplified) == 0:
        return assignment
    
    variable = choose_variable(simplified, assignment)

    true_branch = dict(assignment)
    true_branch[variable] = True
    result = sat_solve(simplified, true_branch)
    if result is not None:
        return result
    
    false_branch = dict(assignment)
    false_branch[variable] = False
    return sat_solve(simplified, false_branch)



def print_result(assignment):
    """Print the SAT result using the assignment handout format."""
    print(f'satisfiable: {str(assignment is not None).lower()}')
    print(f'assignment: {assignment}')


def main():
    """Run the solver from the command line on a CNF formula."""
    raw = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    clauses = ast.literal_eval(raw)
    print_result(sat_solve(clauses, {}))


if __name__ == '__main__':
    main()
