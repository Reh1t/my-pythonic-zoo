"""
test_exact_cover_matrix_example.py
"""

from algorithms.dancing_links.exact_cover_matrix_example import (
    COLUMNS,
    ROWS,
    DataNode,
    add_row,
    create_headers,
)


def test_column_headers_form_a_circular_row() -> None:
    headers = create_headers(COLUMNS)

    assert headers["A"].right is headers["B"]
    assert headers["D"].right is headers["A"]
    assert headers["A"].left is headers["D"]


def test_column_contains_the_expected_choice_nodes() -> None:
    headers = create_headers(COLUMNS)

    for row_name, covered_columns in ROWS.items():
        add_row(headers, row_name, covered_columns)

    first_a_node = headers["A"].down
    second_a_node = first_a_node.down
    assert isinstance(first_a_node, DataNode)
    assert isinstance(second_a_node, DataNode)

    assert first_a_node.row_name == "Choice 1"
    assert second_a_node.row_name == "Choice 3"
    assert second_a_node.down is headers["A"]


def test_choice_nodes_form_a_circular_row() -> None:
    headers = create_headers(COLUMNS)

    for row_name, covered_columns in ROWS.items():
        add_row(headers, row_name, covered_columns)

    choice_1_a = headers["A"].down
    assert isinstance(choice_1_a, DataNode)

    assert choice_1_a.column is headers["A"]
    assert choice_1_a.right.column is headers["B"]
    assert choice_1_a.right.right is choice_1_a
