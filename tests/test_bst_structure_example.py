"""
test_bst_structure_example.py

Test the foundational mental model of a Binary Search Tree (BST).

These tests ensure that the structural rules we teach in the example module
hold true programmatically. We test both correct and deliberately incorrect
structures to prove that our validation logic works.
"""

from algorithms.binary_search_tree.bst_structure_example import Node


def _is_valid_bst(
    node: Node | None,
    min_val: int | float = float("-inf"),
    max_val: int | float = float("inf"),
) -> bool:
    """
    Helper function to mathematically verify the BST ordering rule.

    This function recursively checks that every single node in the tree
    falls strictly within the allowed minimum and maximum values for its
    specific position.
    """
    # A dead end (None) is technically a valid BST.
    if node is None:
        return True

    # If the current node breaks the ordering rule, the tree is invalid.
    if not (min_val < node.value < max_val):
        return False

    # The left child must be smaller than the current node's value.
    # The right child must be larger than the current node's value.
    return _is_valid_bst(node.left, min_val, node.value) and _is_valid_bst(
        node.right, node.value, max_val
    )


# --- Initialization & Structure Tests ---


def test_node_initializes_with_value_and_empty_branches() -> None:
    """A new node should store its value and default to having no children."""
    test_value = 42
    node = Node(test_value)

    assert node.value == test_value
    assert node.left is None
    assert node.right is None


def test_node_can_be_explicitly_linked_to_children() -> None:
    """Nodes should retain the exact references we assign to their left and right."""
    parent = Node(10)
    left_child = Node(5)
    right_child = Node(15)

    parent.left = left_child
    parent.right = right_child

    # We use 'is' to verify it points to the exact same object in memory,
    # not just another node that happens to have the same value.
    assert parent.left is left_child
    assert parent.right is right_child


# --- Invariant & Edge Case Tests ---


def test_single_node_is_valid_bst() -> None:
    """A tree with only one node (no children) is mathematically a valid BST."""
    root = Node(10)
    assert _is_valid_bst(root) is True


def test_manual_bst_satisfies_ordering_rule() -> None:
    """Recreate the example tree and prove it passes the strict invariant check."""
    # This tree matches 'demonstrate_ordering_rule' from the main module.
    root = Node(20)
    root.left = Node(10)
    root.right = Node(30)
    root.left.left = Node(5)
    root.left.right = Node(15)

    assert _is_valid_bst(root) is True


def test_unbalanced_linked_list_satisfies_ordering_rule() -> None:
    """An extreme, unbalanced tree satisfies the rule if values increase."""
    root = Node(10)
    root.right = Node(20)
    root.right.right = Node(30)
    root.right.right.right = Node(40)

    assert _is_valid_bst(root) is True


# --- Failure / Violation Tests ---


def test_invalid_left_child_violates_ordering_rule() -> None:
    """If a left child is larger than its parent, the tree must be flagged invalid."""
    root = Node(10)

    # 20 is larger than 10, so it belongs on the right. Placing it on the
    # left deliberately breaks the core rule of a BST.
    root.left = Node(20)

    assert _is_valid_bst(root) is False


def test_invalid_right_child_violates_ordering_rule() -> None:
    """If a right child is smaller than its parent, the tree must be flagged invalid."""
    root = Node(10)

    # 5 is smaller than 10, so it belongs on the left. Placing it on the
    # right deliberately breaks the rule.
    root.right = Node(5)

    assert _is_valid_bst(root) is False


def test_grandchild_violates_global_ordering_rule() -> None:
    """A node must be valid relative to ALL ancestors, not just its parent."""
    root = Node(20)
    root.left = Node(10)

    # Locally, 25 is greater than 10, so it seems valid as a right child.
    # However, globally, 25 is in the left subtree of 20, so it MUST be < 20.
    # This is a classic BST gotcha that our invariant checker catches.
    root.left.right = Node(25)

    assert _is_valid_bst(root) is False


def test_duplicate_value_violates_strict_ordering_rule() -> None:
    """Duplicate values violate our strict < and > teaching invariant."""
    root = Node(10)

    # We decided our BST does not allow duplicates. If a duplicate is manually
    # forced into the tree, it should fail validation.
    root.left = Node(10)

    assert _is_valid_bst(root) is False
