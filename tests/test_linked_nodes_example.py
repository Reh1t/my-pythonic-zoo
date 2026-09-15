"""
test_linked_nodes_example.py
"""

from algorithms.dancing_links.linked_nodes_example import Node


def test_middle_node_can_be_unlinked_and_relinked() -> None:
    first = Node("A")
    middle = Node("B")
    last = Node("C")

    first.right = middle
    middle.left = first
    middle.right = last
    last.left = middle

    middle.unlink()

    assert first.right is last
    assert last.left is first

    middle.relink()

    assert first.right is middle
    assert last.left is middle


def test_end_node_can_be_unlinked_and_relinked() -> None:
    first = Node("A")
    last = Node("B")

    first.right = last
    last.left = first

    first.unlink()

    assert last.left is None

    first.relink()

    assert last.left is first
