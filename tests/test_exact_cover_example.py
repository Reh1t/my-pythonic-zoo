"""
test_exact_cover_example.py
"""

from algorithms.dancing_links.exact_cover_example import ROWS, is_exact_cover


def test_complete_non_overlapping_rows_are_exact_cover() -> None:
    assert is_exact_cover([ROWS["Choice 1"], ROWS["Choice 2"]]) is True


def test_overlapping_rows_are_not_exact_cover() -> None:
    assert is_exact_cover([ROWS["Choice 1"], ROWS["Choice 3"]]) is False
