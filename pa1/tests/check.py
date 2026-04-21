#!/usr/bin/env python3
"""Self-check for PA1 Horn solver using plaintext fixtures."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def list_fixture_files(tests_dir: Path) -> list[Path]:
    """All .txt files in this directory (sorted for stable order)."""
    return sorted(tests_dir.glob('*.txt'))


def split_fixture(text: str) -> tuple[str, str]:
    marker = '=== EXPECTED ==='
    if marker not in text:
        raise ValueError('Fixture missing === EXPECTED === section')
    left, right = text.split(marker, 1)
    input_text = left.replace('=== INPUT ===', '').strip() + "\n"
    expected_text = right.strip() + "\n"
    return input_text, expected_text


def normalize_output(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.strip().splitlines()).strip() + "\n"


def extract_satisfiable(text: str) -> str | None:
    for line in text.splitlines():
        low = line.strip().lower()
        if low.startswith('satisfiable:'):
            return low.split(':', 1)[1].strip()
    return None


def run_case(solution_path: Path, fixture_path: Path) -> tuple[bool, str]:
    raw = fixture_path.read_text(encoding='utf-8')
    input_text, expected_text = split_fixture(raw)
    clause_arg = input_text.strip()

    proc = subprocess.run(
        [sys.executable, str(solution_path), clause_arg],
        text=True,
        capture_output=True,
    )
    if proc.returncode != 0:
        return False, f'non-zero exit ({proc.returncode}) stderr={proc.stderr.strip()!r}'

    got = normalize_output(proc.stdout)
    want = normalize_output(expected_text)
    got_sat = extract_satisfiable(got)
    want_sat = extract_satisfiable(want)
    if got_sat is None:
        return False, 'missing `satisfiable:` line in output'
    if want_sat is None:
        return False, 'fixture missing `satisfiable:` line'
    if got_sat != want_sat:
        return False, f'expected satisfiable={want_sat!r}, got satisfiable={got_sat!r}'
    return True, 'OK'


def resolve_solution_path(student_root: Path, arg: str) -> Path:
    """
    Resolve --solution so it works from any cwd (e.g. running check.py from tests/).

    Relative paths: try cwd first, then student/ (so default pa1.py works from student/).
    """
    p = Path(arg).expanduser()
    if p.is_absolute():
        return p.resolve()
    cwd_candidate = (Path.cwd() / p).resolve()
    if cwd_candidate.exists():
        return cwd_candidate
    student_candidate = (student_root / p).resolve()
    if student_candidate.exists():
        return student_candidate
    return cwd_candidate


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--solution', '--student', dest='solution', default='pa1.py')
    args = parser.parse_args()

    student_root = Path(__file__).resolve().parents[1]
    tests_dir = Path(__file__).resolve().parent
    solution_path = resolve_solution_path(student_root, args.solution)

    if not solution_path.exists():
        print(f'Solution file not found: {solution_path}')
        print(
            '  Relative --solution paths are resolved from your shell cwd first, '
            f'then from {student_root}.'
        )
        sys.exit(1)

    fixtures = list_fixture_files(tests_dir)
    if not fixtures:
        print('No .txt fixture files found in tests directory')
        sys.exit(1)

    failed = False
    for path in fixtures:
        ok, msg = run_case(solution_path, path)
        label = path.stem.removeprefix('case_')
        if ok:
            print(f'{label}: OK')
        else:
            print(f'{label}: FAIL ({msg})')
            failed = True

    sys.exit(1 if failed else 0)


if __name__ == '__main__':
    main()
