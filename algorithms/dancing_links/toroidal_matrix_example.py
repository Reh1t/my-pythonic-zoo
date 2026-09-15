"""
toroidal_matrix_example.py

Combine horizontal and vertical circular links into the four-way structure
used by Dancing Links.

The previous Circular Links exhibit demonstrated row and column circles
separately. This exhibit combines those ideas so every node participates in
both structures at the same time: left and right links connect across a row,
while up and down links connect through a column.

When the outer edges wrap around in both directions, the structure is called
toroidal because following links far enough eventually returns to the starting
point, like moving around the surface of a torus.

Readers should first understand linked_nodes_example.py and
circular_links_example.py. This exhibit focuses only on combining those links
into a matrix; cover/uncover operations and Algorithm X integration come later.

Toroidal structures also appear in simulations, games, and mathematical models
where boundaries wrap around. Here, however, the toroidal linked matrix has a
more specialised purpose: it represents an Exact Cover problem so Dancing Links
can efficiently remove and restore parts of that structure during its search.
Sudoku itself is not toroidal; its constraints are first encoded as Exact Cover.
"""


class Node:
    """Represent one node linked in four circular directions."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.left: Node = self
        self.right: Node = self
        self.up: Node = self
        self.down: Node = self

    def link_right(self, neighbour: "Node") -> None:
        """Link this node and another node together horizontally."""
        self.right = neighbour
        neighbour.left = self

    def link_down(self, neighbour: "Node") -> None:
        """Link this node and another node together vertically."""
        self.down = neighbour
        neighbour.up = self


if __name__ == "__main__":
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

    print("\n=== DEMONSTRATION: TOROIDAL MATRIX ===")

    print(f"    A right -> B: {top_left.right is top_right}")
    print(f"    B right wraps -> A: {top_right.right is top_left}")

    print(f"    A down -> C: {top_left.down is bottom_left}")
    print(f"    C down wraps -> A: {bottom_left.down is top_left}")

    print(f"    D left -> C: {bottom_right.left is bottom_left}")
    print(f"    D up -> B: {bottom_right.up is top_right}")

    print("\n=== STRUCTURE SUMMARY ===")
    print(
        """
    Each node now belongs to both a circular row and a circular column:

        A <-> B
        ↕     ↕
        C <-> D

    Horizontal links wrap left <-> right.
    Vertical links wrap up <-> down.
    """
    )

    print()
