"""
test_cover_uncover_example.py
"""

from algorithms.dancing_links.cover_uncover_example import Node


def test_horizontal_unlink_and_relink_are_reversible() -> None:
    left = Node("A")
    right = Node("B")

    left.link_right(right)
    right.link_right(left)

    right.unlink_horizontal()

    assert left.right is left
    assert right.left is left

    right.relink_horizontal()

    assert left.right is right


def test_vertical_unlink_and_relink_are_reversible() -> None:
    top = Node("A")
    bottom = Node("B")

    top.link_down(bottom)
    bottom.link_down(top)

    bottom.unlink_vertical()

    assert top.down is top
    assert bottom.up is top

    bottom.relink_vertical()

    assert top.down is bottom
