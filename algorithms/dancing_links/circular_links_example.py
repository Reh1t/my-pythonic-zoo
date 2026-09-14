"""
circular_links_example.py

Extend the previous doubly linked chain into a circular linked structure.

The linked-nodes example used None at the ends of the chain because the first
node had no left neighbour and the last node had no right neighbour. Dancing
Links avoids those end cases by linking the final node back to the first and
the first node back to the final one.

In a circular doubly linked structure, every node always has both a left and a
right neighbour. That removes the special-case checks needed at the ends of a
linear chain and makes unlinking and restoring nodes more uniform.

This example builds directly on the object-reference relationships introduced
in linked_nodes_example.py. Readers unfamiliar with doubly linked nodes should
work through that exhibit first and understand how nodes are linked, unlinked,
and restored before continuing with circular links here.

This example demonstrates circular links in both directions separately:
horizontal links model movement across a row, while vertical links model
movement down a column. The following Toroidal Matrix exhibit will combine
those ideas so each node participates in both circular structures at once,
forming the four-way toroidal matrix that Dancing Links will later operate on.
"""


class Node:
    """
    Represent one node with circular links to neighbouring nodes.

    Unlike the previous linear chain, a newly created circular node does not
    use None for missing neighbours. It initially links back to itself instead.
    A single node therefore already forms a valid one-node circle.

    As other nodes are connected, these references will be replaced with the
    appropriate neighbours while the structure remains circular.
    """

    def __init__(self, name: str) -> None:
        self.name = name

        # A new circular node begins by pointing to itself in every direction
        # currently supported by this example.
        self.left: Node = self
        self.right: Node = self
        self.up: Node = self
        self.down: Node = self


if __name__ == "__main__":
    print("\n=== DEMONSTRATION: HORIZONTAL CIRCULAR LINKS ===")

    first = Node("A")
    middle = Node("B")
    last = Node("C")

    # Link A - B - C horizontally, then connect the ends so the row becomes
    # circular: A <-> B <-> C <-> A.
    first.right = middle
    middle.left = first
    middle.right = last
    last.left = middle
    last.right = first
    first.left = last

    print(f"A's right neighbour is B: {first.right is middle}")
    print(f"B's right neighbour is C: {middle.right is last}")
    print(f"C's right neighbour wraps back to A: {last.right is first}")
    print(f"A's left neighbour wraps back to C: {first.left is last}")

    print("\n=== DEMONSTRATION: VERTICAL CIRCULAR LINKS ===")

    top = Node("A")
    centre = Node("B")
    bottom = Node("C")

    # Link A - B - C vertically, then connect the ends so the column becomes
    # circular: A <-> B <-> C <-> A.
    top.down = centre
    centre.up = top
    centre.down = bottom
    bottom.up = centre
    bottom.down = top
    top.up = bottom

    print(f"A's lower neighbour is B: {top.down is centre}")
    print(f"B's lower neighbour is C: {centre.down is bottom}")
    print(f"C's lower neighbour wraps back to A: {bottom.down is top}")
    print(f"A's upper neighbour wraps back to C: {top.up is bottom}")

    print()
