"""
dancing_links_example.py

Combine the preceding study sequence into a complete Dancing Links (DLX)
demonstration.

Algorithm X is the search algorithm; Dancing Links is a specialised way of
implementing it. Algorithm X defines the decisions the search must make:
choose a requirement, try a compatible choice, continue recursively, and
backtrack when necessary. Dancing Links supplies the linked data structure and
the reversible cover/uncover operations used to carry out those steps
efficiently. It does not replace or extend Algorithm X; it implements the same
search while managing the changing Exact Cover problem differently.

In short:
    Exact Cover = the problem
    Algorithm X = the search algorithm
    Dancing Links (DLX) = an efficient implementation technique for Algorithm X

The earlier Algorithm X exhibit created new sets and dictionaries to represent
the reduced problem at each recursive branch. Here, one toroidal linked matrix
is built and then modified reversibly throughout the search instead. During
the search, cover operations temporarily unlink requirements and conflicting
choices from that active structure. When Algorithm X backtracks, uncover
operations restore the same links in reverse order.

The result is the same search expressed through reversible structural changes:

    Algorithm X example:
        choose -> build reduced collections -> recurse -> discard

    Dancing Links example:
        choose -> cover links -> recurse -> uncover links

This exhibit deliberately reuses the same four-requirement, four-choice Exact
Cover problem as the earlier examples. The expected solutions therefore remain
Choice 1 + Choice 2 and Choice 3 + Choice 4. Keeping the problem unchanged makes
it possible to compare the implementations directly rather than learning a new
problem at the same time.

Readers should work through and understand the complete Dancing Links Study
Sequence in algorithms/README.md before continuing here. This final exhibit
assumes familiarity with Exact Cover, Algorithm X, linked and circular nodes,
the toroidal matrix, reversible cover/uncover operations, and the linked Exact
Cover matrix representation.
"""


class ColumnHeader:
    """Represent one Exact Cover requirement and its active column."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.left: ColumnHeader = self
        self.right: ColumnHeader = self
        self.up: ColumnHeader | DataNode = self
        self.down: ColumnHeader | DataNode = self
        self.size = 0


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

ROOT_NAME = "ROOT"


def create_headers(column_names: list[str]) -> dict[str, ColumnHeader]:
    """
    Create the circular header row, including a permanent root sentinel.

    The root is not an Exact Cover requirement and is never covered. It provides
    the search with a stable entry point into the changing circle of active column
    headers, even after the first requirement column has been removed.
    """
    all_names = [ROOT_NAME, *column_names]
    headers = {name: ColumnHeader(name) for name in all_names}

    for index, name in enumerate(all_names):
        current = headers[name]
        current.left = headers[all_names[index - 1]]
        current.right = headers[all_names[(index + 1) % len(all_names)]]

    return headers


def add_row(
    headers: dict[str, ColumnHeader],
    row_name: str,
    covered_columns: set[str],
) -> None:
    """Create and link the data nodes for one Exact Cover row."""
    nodes = [DataNode(row_name, headers[name]) for name in sorted(covered_columns)]

    for index, node in enumerate(nodes):
        node.left = nodes[index - 1]
        node.right = nodes[(index + 1) % len(nodes)]

        header = node.column
        node.up = header.up
        node.down = header
        header.up.down = node
        header.up = node

        # Record that another active data node has been inserted into
        # that requirement's column
        header.size += 1


def build_matrix() -> dict[str, ColumnHeader]:
    """Build the linked Exact Cover matrix used by the DLX search."""
    headers = create_headers(COLUMNS)

    for row_name, covered_columns in ROWS.items():
        add_row(headers, row_name, covered_columns)

    return headers


def cover(column: ColumnHeader) -> None:
    """Temporarily remove a requirement and its conflicting choices."""
    column.right.left = column.left
    column.left.right = column.right

    row = column.down

    while row is not column:
        assert isinstance(row, DataNode)

        node = row.right

        while node is not row:
            node.down.up = node.up
            node.up.down = node.down
            node.column.size -= 1

            node = node.right

        row = row.down


def uncover(column: ColumnHeader) -> None:
    """Restore a previously covered requirement and its conflicting choices."""
    row = column.up

    while row is not column:
        assert isinstance(row, DataNode)

        node = row.left

        while node is not row:
            node.column.size += 1
            node.down.up = node
            node.up.down = node

            node = node.left

        row = row.up

    column.right.left = column
    column.left.right = column


def choose_column(headers: dict[str, ColumnHeader]) -> ColumnHeader | None:
    """
    Choose the smallest currently active column for the next search step:
    Start at ROOT, look only at currently linked headers, keep the smallest
    active column seen and return it
    """
    root = headers[ROOT_NAME]
    current = root.right

    if current is root:
        return None

    assert isinstance(current, ColumnHeader)
    chosen = current
    current = current.right

    while current is not root:
        assert isinstance(current, ColumnHeader)

        if current.size < chosen.size:
            chosen = current

        current = current.right

    return chosen


def cover_row_columns(row: DataNode) -> None:
    """Cover the other requirement columns satisfied by a selected row."""
    node = row.right

    while node is not row:
        cover(node.column)
        node = node.right


def uncover_row_columns(row: DataNode) -> None:
    """Restore the other requirement columns satisfied by a selected row."""
    node = row.left

    while node is not row:
        uncover(node.column)
        node = node.left


def search(
    headers: dict[str, ColumnHeader],
    partial_solution: list[str],
    solutions: list[list[str]],
) -> None:
    """Search the linked Exact Cover matrix using Algorithm X and DLX."""

    # Algorithm X: choose a requirement
    column = choose_column(headers)

    if column is None:
        solutions.append(partial_solution.copy())
        return

    # DLX: cover its linked column
    cover(column)

    # The column's candidate rows remain reachable through column.down,
    # even though its header is no longer in the active header ring.
    row = column.down

    # Algorithm X: try each available choice;
    # DLX covers and restores its columns.
    while row is not column:
        assert isinstance(row, DataNode)
        partial_solution.append(row.row_name)  # append choice
        cover_row_columns(row)
        search(headers, partial_solution, solutions)
        uncover_row_columns(row)
        partial_solution.pop()  # pop choice
        row = row.down  # next choice

    # DLX: uncover its linked column
    uncover(column)


if __name__ == "__main__":
    headers = build_matrix()
    solutions: list[list[str]] = []

    search(headers, [], solutions)

    print("\n=== DEMONSTRATION: DANCING LINKS ===")
    for solution in solutions:
        print(f"    Exact cover found: {solution}")

    print("\n=== SEARCH SUMMARY ===")
    print(
        """
    Algorithm X chooses requirements and candidate rows.

    Dancing Links manages the changing Exact Cover matrix:

        choose column
            ↓
        cover linked structure
            ↓
        choose row
            ↓
        cover row's other columns
            ↓
        recurse
            ↓
        uncover in reverse order
            ↓
        backtrack

    The same linked matrix is modified and restored throughout the search.
    """
    )

    print()
