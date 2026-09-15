"""
linked_nodes_example.py

Introduce the linked-node idea that Dancing Links depends on.

Algorithm X repeatedly removes conflicting choices while it explores a search
path, then needs those choices again if it backtracks. Ordinary Python
collections can model that process, but Dancing Links uses linked nodes so
items can be disconnected and later restored by changing only neighbouring
references.

Linked structures are a general computer-science technique rather than a
Python-specific feature. Languages may represent the links differently; this
Python example uses object references between Node instances rather than
working directly with memory pointers. Python does not inherently make linked
nodes more efficient, but its managed object references make them easier and
safer to express. That also makes Python useful for demonstrating the idea:
relationships such as `node.left` and `node.right` can be inspected directly
without manual memory management obscuring the underlying linked structure.

This example focuses on that behaviour in isolation. It uses a small doubly
linked chain and deliberately avoids circular links, four-way matrix links,
Algorithm X, and Sudoku. The goal is to understand how one node can be removed
without destroying the relationships needed to put it back.
"""


class Node:
    """
    Represent one item in a doubly linked chain.

    A newly created node is not connected to any neighbours, so both links
    initially contain None. The type hint `Node | None` means each attribute
    may later refer to another Node object, but is also allowed to contain None
    when no neighbour exists. For example, the first node in a non-circular
    chain has no left neighbour and the last node has no right neighbour.
    """

    def __init__(self, name: str) -> None:
        self.name = name
        self.left: Node | None = None
        self.right: Node | None = None

    def unlink(self) -> None:
        """Remove this node from the active chain without deleting the node."""
        if self.left is not None:
            self.left.right = self.right
        if self.right is not None:
            self.right.left = self.left

    def relink(self) -> None:
        """Restore this node between its remembered left and right neighbours."""
        if self.left is not None:
            self.left.right = self
        if self.right is not None:
            self.right.left = self


if __name__ == "__main__":
    first = Node("A")
    middle = Node("B")
    last = Node("C")

    # Link nodes A <-> B <-> C
    first.right = middle
    middle.left = first
    middle.right = last
    last.left = middle

    print("\n=== DEMONSTRATION: DOUBLY LINKED NODES ===")
    print(f"    A's right neighbour is B: {first.right is middle}")
    print(f"    B's left neighbour is A: {middle.left is first}")
    print(f"    B's right neighbour is C: {middle.right is last}")
    print(f"    C's left neighbour is B: {last.left is middle}")

    # Make A left of C, with the middle variable still referring
    # to the B object, so A <-> C directly.  B will not be destroyed.
    middle.unlink()

    print(f"\n    After unlinking B, A's right neighbour is C: {first.right is last}")
    print(f"    After unlinking B, C's left neighbour is A: {last.left is first}")
    print(f"    B still exists as a Node object: {middle.name == 'B'}")

    # Restore the nodes to A <-> B <-> C
    middle.relink()

    print(f"\n    After restoring B, A's right neighbour is B: {first.right is middle}")
    print(f"    After restoring B, C's left neighbour is B: {last.left is middle}")

    print("\n=== STRUCTURE SUMMARY ===")
    print(
        """
    Original:
        A <-> B <-> C

    B unlinked:
        A <------> C       B still exists

    B restored:
        A <-> B <-> C
    """
    )

    print()
