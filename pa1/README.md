# PA1: Horn Formula Satisfiability Solver

## Collaborators
- Kamron Swingle
- Jun Yi

## Overview
This program determines whether a propositional Horn formula is satisfiable using the **forward chaining** (unit propagation) algorithm. Horn clauses are a special case of SAT where each clause has at most one positive literal, allowing efficient solving without backtracking.

## How It Works

Each Horn clause is interpreted as an implication:
- `[a]` → fact: `a` is true
- `[-a, -b, c]` → if `a` and `b` then `c`
- `[-d]` → if `d` then `false` (contradiction rule)

The solver:
1. Seeds the worklist with all known facts
2. Tracks how many body literals remain unmet for each rule
3. When a variable is proven true, decrements the counter for all rules containing it
4. When a rule's body is fully satisfied, derives its head (or reports unsatisfiable if the head is `None`)
5. If propagation reaches a fixed point with no contradiction, the formula is satisfiable

## Usage

```bash
python3 pa1.py "[[a],[b],[-a,-b,c],[-c,d],[-d]]"
```

### Output
```
satisfiable: false
```

```bash
python3 pa1/pa1.py "[[a],[b],[-a,-b,c],[-c,d]]"
```

## Running Tests

From the project root:

```bash
python3 tests/check.py --solution pa1.py
```

## Example

Given the formula `[[a],[b],[-a,-b,c],[-c,d],[-d]]`:

| Clause | Meaning |
|---|---|
| `[a]` | fact: `a` is true |
| `[b]` | fact: `b` is true |
| `[-a,-b,c]` | if `a` and `b` then `c` |
| `[-c,d]` | if `c` then `d` |
| `[-d]` | if `d` then `false` |

Trace:
1. Mark `a` and `b` as true from facts
2. Fire `a ∧ b → c`, derive `c`
3. Fire `c → d`, derive `d`
4. Fire `d → false`, contradiction — **unsatisfiable**