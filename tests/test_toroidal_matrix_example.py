"""
test_toroidal_matrix_example.py
"""

from algorithms.dancing_links.toroidal_matrix_example import Node


def test_nodes_wrap_horizontally_and_vertically() -> None:
    top_left = Node("A")
    top_right = Node("B")
    bottom_left = Node("C")
    bottom_right = Node("D")

    top_left.link_right(top_right)
    top_right.link_right(top_left)
    bottom_left.link_right(bottom_right)
    bottom_right.link_right(bottom_left)

    top_left.link_down(bottom_left)
    bottom_left.link_down(top_left)
    top_right.link_down(bottom_right)
    bottom_right.link_down(top_right)

    assert top_left.right is top_right
    assert top_right.right is top_left
    assert top_left.down is bottom_left
    assert bottom_left.down is top_left
    assert bottom_right.left is bottom_left
    assert bottom_right.up is top_right
