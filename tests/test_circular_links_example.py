"""
test_circular_links_example.py
"""

from algorithms.dancing_links.circular_links_example import Node


def test_horizontal_nodes_form_a_circle() -> None:
    first = Node("A")
    middle = Node("B")
    last = Node("C")

    first.right = middle
    middle.left = first
    middle.right = last
    last.left = middle
    last.right = first
    first.left = last

    assert first.right is middle
    assert middle.right is last
    assert last.right is first
    assert first.left is last


def test_vertical_nodes_form_a_circle() -> None:
    top = Node("A")
    centre = Node("B")
    bottom = Node("C")

    top.down = centre
    centre.up = top
    centre.down = bottom
    bottom.up = centre
    bottom.down = top
    top.up = bottom

    assert top.down is centre
    assert centre.down is bottom
    assert bottom.down is top
    assert top.up is bottom
