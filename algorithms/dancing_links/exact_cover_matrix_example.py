"""
exact_cover_matrix_example.py

Translate an Exact Cover problem into the linked matrix structure that Dancing
Links will later search.

The earlier Exact Cover and Algorithm X exhibits represented requirements and
choices using ordinary Python sets and dictionaries. The linked-node exhibits
then introduced the four-way toroidal structure and reversible cover/uncover
operations independently. This exhibit connects those two halves.

Each Exact Cover requirement becomes a column header. Each available choice
becomes a matrix row containing a data node only where that choice satisfies a
requirement. Those data nodes are linked horizontally across their row and
vertically beneath their corresponding column header.

The familiar four-choice problem is reused here so the representation is the
only new idea:

    Choice 1 covers A and B
    Choice 2 covers C and D
    Choice 3 covers A and C
    Choice 4 covers B and D

This exhibit builds and inspects that linked matrix but does not search it.
The following Dancing Links exhibit will apply Algorithm X and the reversible
cover/uncover operations to this structure.

Readers should first understand exact_cover_example.py, linked_nodes_example.py,
circular_links_example.py, toroidal_matrix_example.py, and
cover_uncover_example.py before continuing here. This exhibit deliberately
builds on those concepts rather than re-teaching them, so understanding the
earlier progression is recommended before examining how they are combined into
an Exact Cover matrix.
"""


class ColumnHeader:
    """Represent one Exact Cover requirement at the top of a matrix column."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.left: ColumnHeader = self
        self.right: ColumnHeader = self
        self.up: ColumnHeader | DataNode = self
        self.down: ColumnHeader | DataNode = self


class DataNode:
    """Represent one matrix intersection where a choice satisfies a requirement."""

    def __init__(self, row_name: str, column: ColumnHeader) -> None:
        self.row_name = row_name
        self.column = column
        self.left: DataNode = self
        self.right: DataNode = self
        self.up: ColumnHeader | DataNode = self
        self.down: ColumnHeader | DataNode = self


COLUMNS = ["A", "B", "C", "D"]

ROWS = {
    "Choice 1": {"A", "B"},
    "Choice 2": {"C", "D"},
    "Choice 3": {"A", "C"},
    "Choice 4": {"B", "D"},
}


def create_headers(column_names: list[str]) -> dict[str, ColumnHeader]:
    """Create one linked column header for each Exact Cover requirement."""

    # A dictionary comprehension creates one ColumnHeader object for each name.
    headers = {name: ColumnHeader(name) for name in column_names}

    # enumerate() provides both the position and name of each column.
    # Modulo (%) keeps the calculated position within the valid repeating indexes
    # 0, 1, 2, 3, 0..., so the final right-hand link wraps back to the first column.
    for index, name in enumerate(column_names):
        current = headers[name]
        current.left = headers[column_names[index - 1]]
        current.right = headers[column_names[(index + 1) % len(column_names)]]

    return headers


def add_row(
    headers: dict[str, ColumnHeader],
    row_name: str,
    covered_columns: set[str],
) -> list[DataNode]:
    """Create and link the data nodes for one Exact Cover row."""
    nodes = [DataNode(row_name, headers[name]) for name in sorted(covered_columns)]
    for index, node in enumerate(nodes):
        node.left = nodes[index - 1]
        node.right = nodes[(index + 1) % len(nodes)]
        header = node.column

        # Insert this node at the bottom of its circular column. Point the new
        # node up to the current last node and down to the header, then update
        # those two neighbours so they point back to the new node.
        # For the first insertion, the resulting vertical circle is A <-> node <-> A.
        node.up = header.up
        node.down = header
        header.up.down = node
        header.up = node

    return nodes


if __name__ == "__main__":
    headers = create_headers(COLUMNS)

    for row_name, covered_columns in ROWS.items():
        add_row(headers, row_name, covered_columns)

    print("\n=== DEMONSTRATION: EXACT COVER MATRIX HEADERS ===")
    print(f"    A's right header is B: {headers['A'].right is headers['B']}")
    print(f"    D's right header wraps to A: {headers['D'].right is headers['A']}")
    print(f"    A's left header wraps to D: {headers['A'].left is headers['D']}")

    first_a_node = headers["A"].down

    # Assert the expected node type as an internal invariant. This also narrows
    # the union type for mypy; assert is, here and in the following usages, not
    # a substitute for input validation.
    assert isinstance(first_a_node, DataNode)
    second_a_node = first_a_node.down
    assert isinstance(second_a_node, DataNode)

    print("\n=== DEMONSTRATION: DATA NODES IN COLUMN A ===")
    print(f"    First node below A belongs to: {first_a_node.row_name}")
    print(f"    Second node below A belongs to: {second_a_node.row_name}")
    print(
        "    Column A then wraps back to its header:"
        f" {headers['A'].down.down.down is headers['A']}"
    )

    choice_1_a = headers["A"].down
    assert isinstance(choice_1_a, DataNode)

    print("\n=== DEMONSTRATION: DATA NODES IN CHOICE 1 ===")
    print(f"    Choice 1 starts in column A: {choice_1_a.column is headers['A']}")
    print(
        f"    Moving right reaches column B: {choice_1_a.right.column is headers['B']}"
    )
    print(
        "    Moving right again wraps back to A:"
        f" {choice_1_a.right.right is choice_1_a}"
    )

    print("\n=== LINKED MATRIX CREATED ===")
    print(
        """
    A       B       C       D
    ↕       ↕       ↕       ↕
    1 ↔──── 1       2 ↔──── 2
    ↕       ↕       ↕       ↕
    3 ↔──────────── 3
            4 ↔──────────── 4
    ↕       ↕       ↕       ↕
    wraps   wraps   wraps   wraps
    """
    )

    print()
