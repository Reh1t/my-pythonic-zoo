"""
cover_uncover_example.py

Demonstrate the reversible cover and uncover operations that make Dancing Links
efficient during Algorithm X backtracking.

The earlier Algorithm X example created new sets and dictionaries for every
search branch. When a row was selected, it built a smaller collection of
remaining columns and rows, then passed those new objects into the next
recursive call. That approach is clear and works well for teaching, but repeated
copying and rebuilding becomes increasingly expensive as the search grows.

The main saving is processing work: cover and uncover update a small number of
links instead of repeatedly rebuilding large collections during backtracking.
They also reduce temporary memory allocation because fewer short-lived sets and
dictionaries need to be created. The linked structure itself still has memory
overhead, however, because every node stores several references, so Dancing
Links should not simply be described as using less memory overall.

Dancing Links takes a different approach. Instead of creating a new reduced
matrix for each branch, it temporarily disconnects parts of the existing
toroidal matrix. The disconnected nodes are not destroyed: their own links
still remember enough of the surrounding structure for them to be restored
later.

A cover operation temporarily removes a constraint and the conflicting choices
that can no longer participate in the current search path. Algorithm X can then
continue through the smaller active structure. If that path reaches a dead end,
backtracking performs the corresponding uncover operation to restore the matrix
to its previous state before another choice is tried.

This reversibility is the central idea behind the name Dancing Links: links
appear to move out of and back into the active structure as the recursive search
advances and backtracks.

Readers should first understand exact_cover_example.py, algorithm_x_example.py,
linked_nodes_example.py, circular_links_example.py, and
toroidal_matrix_example.py. This exhibit focuses on reversible structural
changes; the following Dancing Links solver exhibit will combine these
operations with Algorithm X to solve Exact Cover problems.
"""


class Node:
    """Represent one node whose four links can be changed and restored."""

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

    def unlink_horizontal(self) -> None:
        """Temporarily remove this node from its circular row."""
        self.left.right = self.right
        self.right.left = self.left

    def relink_horizontal(self) -> None:
        """Restore this node between its remembered horizontal neighbours."""
        self.left.right = self
        self.right.left = self

    def unlink_vertical(self) -> None:
        """Temporarily remove this node from its circular column."""
        self.up.down = self.down
        self.down.up = self.up

    def relink_vertical(self) -> None:
        """Restore this node between its remembered vertical neighbours."""
        self.up.down = self
        self.down.up = self


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

    print("\n=== DEMONSTRATION: COVER / UNCOVER ===")
    print(
        f"\n    Before cover, A's right neighbour is B: {top_left.right is top_right}"
    )

    top_right.unlink_horizontal()

    print(
        f"\n    After cover, A's right neighbour skips B: {top_left.right is top_left}"
    )
    print(f"    B still remembers A on its left: {top_right.left is top_left}")

    top_right.relink_horizontal()

    print(
        "\n    After uncover, A's right neighbour is B again:"
        f" {top_left.right is top_right}"
    )

    print("\n=== STRUCTURE SUMMARY ===")
    print(
        """
    Before cover:
        A <-> B

    After covering B:
        A <-> A       B still remembers where it belongs

    After uncovering B:
        A <-> B

    The original linked structure has been restored.
    """
    )

    print()
