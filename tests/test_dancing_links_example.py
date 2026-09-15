"""
test_dancing_links_example.py
"""

from algorithms.dancing_links.dancing_links_example import (
    ROOT_NAME,
    build_matrix,
    choose_column,
    cover,
    search,
    uncover,
)

INITIAL_COLUMN_SIZE = 2


def test_cover_removes_column_and_conflicting_nodes() -> None:
    headers = build_matrix()

    cover(headers["A"])

    assert headers["B"].left is headers[ROOT_NAME]
    assert headers["D"].right is headers[ROOT_NAME]
    assert headers["B"].size == 1
    assert headers["C"].size == 1


def test_uncover_restores_the_original_structure() -> None:
    headers = build_matrix()

    cover(headers["A"])
    uncover(headers["A"])

    assert headers["A"].left is headers[ROOT_NAME]
    assert headers["A"].right is headers["B"]
    assert headers["B"].size == INITIAL_COLUMN_SIZE
    assert headers["C"].size == INITIAL_COLUMN_SIZE


def test_choose_column_selects_smallest_active_column() -> None:
    headers = build_matrix()

    chosen = choose_column(headers)

    assert chosen is headers["A"]

    cover(headers["A"])
    chosen = choose_column(headers)

    assert chosen is headers["B"]


def test_search_finds_all_exact_covers() -> None:
    headers = build_matrix()
    solutions: list[list[str]] = []

    search(headers, [], solutions)

    assert solutions == [
        ["Choice 1", "Choice 2"],
        ["Choice 3", "Choice 4"],
    ]


def test_search_restores_matrix_after_backtracking() -> None:
    headers = build_matrix()
    solutions: list[list[str]] = []

    search(headers, [], solutions)

    assert headers["A"].right is headers["B"]
    assert headers["A"].left is headers[ROOT_NAME]
    assert headers["A"].size == INITIAL_COLUMN_SIZE
    assert headers["B"].size == INITIAL_COLUMN_SIZE
    assert headers["C"].size == INITIAL_COLUMN_SIZE
    assert headers["D"].size == INITIAL_COLUMN_SIZE
