"""
test_algorithm_x_example.py
"""

from algorithms.dancing_links.algorithm_x_example import (
    COLUMNS,
    ROWS,
    solve_exact_cover,
)


def test_algorithm_x_finds_both_exact_covers_in_deterministic_order() -> None:
    assert solve_exact_cover(COLUMNS, ROWS, []) == [
        ["Choice 1", "Choice 2"],
        ["Choice 3", "Choice 4"],
    ]


def test_algorithm_x_returns_no_solution_when_exact_cover_is_impossible() -> None:
    columns = {"A", "B", "C"}
    rows = {"Choice 1": {"A", "B"}}

    assert solve_exact_cover(columns, rows, []) == []
