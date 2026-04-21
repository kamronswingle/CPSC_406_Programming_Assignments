#!/usr/bin/env python3
"""Student starter for PA1."""
from __future__ import annotations
from collections import deque
from typing import Any, Dict, List
import re
import sys

"""
Sample input: "[[a], [b], [-a,-b,c], [-c,d], [-d]]"
Facts: ['a', 'b']
Rules:
    [-a,-b,c] -> if a and b are true then c.
    [-c,d] -> if c is true then d
    [-d] -> if d is true then false
'variables': ['a', 'b', 'c', 'd'],
'facts': ['a', 'b'],
'rules': [
        {'body': ['a', 'b'], 'head': 'c'},   # Rule 1: a & b -> c
        {'body': ['c'],      'head': 'd'},   # Rule 2: c -> d
        {'body': ['d'],      'head': None}   # Rule 3: d -> False
    ]
rule_counts:
1. {'body': {'a', 'b'}, 'remaining': 2, 'head': 'c'}
2. {'body': {'c'}, 'remaining': 1, 'head': 'd'}
3. {'body': {'d'}, 'remaining': 1, 'head': None}
Step-by-step
pop a from facts
if current (a) is in the rule body --> true
subtract 1 from the remaining
if remaining is zero, and the head is none, say it is unsatisfiable
"""

def solve_horn(formula: Dict[str, Any]) -> Dict[str, Any]:
    true_vars = set(formula['facts'])  # Storage of everything proven true
    worklist = deque(formula['facts'])

    rule_counts = []
    for rule in formula['rules']:
        rule_counts.append({
            'body': set(rule['body']),
            'remaining': len(rule['body']),
            'head': rule['head']
        })

    # Handle rules already fully satisfied before propagation (e.g. empty clause [])
    for rule in rule_counts:
        if rule['remaining'] == 0:
            if rule['head'] is None:
                return {"satisfiable": False, "true_vars": []}
            if rule['head'] not in true_vars:
                true_vars.add(rule['head'])
                worklist.append(rule['head'])

    while worklist:
        current = worklist.popleft()
        for rule in rule_counts:
            if current in rule['body']:
                rule['remaining'] -= 1
                if rule['remaining'] == 0:
                    if rule['head'] is None:
                        return {"satisfiable": False, "true_vars": []}
                    if rule['head'] not in true_vars:
                        true_vars.add(rule['head'])
                        worklist.append(rule['head'])

    return {
        "satisfiable": True,
        "true_vars": list(true_vars)
    }


def parse_horn_clause_string(text: str) -> Dict[str, Any]:
    """
    Parse text like: [[-a,-b,c], [-c,-d,e], [a]]
    Each clause must be Horn (at most one positive literal).
    """
    src = ''.join(text.strip().split())
    clause_texts = re.findall(r'\[([^\[\]]*)\]', src)

    clauses: List[List[str]] = []
    for raw in clause_texts:
        if raw == '':
            clauses.append([])
            continue
        tokens = [tok for tok in raw.split(',') if tok]
        clauses.append(tokens)

    variables = set()
    facts: List[str] = []
    rules: List[Dict[str, Any]] = []

    for clause in clauses:
        neg_body: List[str] = []
        positives: List[str] = []

        for lit in clause:
            if lit.startswith('-'):
                v = lit[1:]
                if v:
                    neg_body.append(v)
                    variables.add(v)
            else:
                positives.append(lit)
                if lit:
                    variables.add(lit)

        head = positives[0] if positives else None

        if not neg_body and head is not None:
            facts.append(head)
        else:
            rules.append({'body': neg_body, 'head': head})

    return {
        'variables': sorted(variables),
        'facts': sorted(set(facts)),
        'rules': rules,
    }


def format_result(result: Dict[str, Any]) -> str:
    sat = 'true' if result['satisfiable'] else 'false'
    if result['satisfiable']:
        tv = ' '.join(sorted(set(result['true_vars'])))
        return f'satisfiable: {sat}\ntrue_vars: {tv}'.rstrip()
    return f'satisfiable: {sat}'


def main() -> None:
    raw = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    formula = parse_horn_clause_string(raw)
    result = solve_horn(formula)
    print(format_result(result))


if __name__ == '__main__':
    main()