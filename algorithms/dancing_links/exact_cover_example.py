"""
exact_cover_example.py

Introduce the Exact Cover problem that Dancing Links is designed to solve.

An exact cover selects rows from a set of possibilities so that every required
column is covered exactly once. This example uses ordinary Python data
structures only. It deliberately avoids Algorithm X and Dancing Links so the
problem can be understood before introducing the solving technique.

This example defines four required columns, A through D, and four available
row choices: AB, CD, AC, and BD. The rows are the choices supplied by this
particular problem; they are not every possible combination of the columns.
There are two exact-cover solutions: choosing AB with CD, or choosing AC with
BD. In either solution, A, B, C, and D are each covered exactly once.

Real-world exact-cover problems arise when a set of requirements must each be
satisfied exactly once by selecting from a collection of available choices.
Exact Cover is fundamentally a constraint-selection technique, not a
data-discovery technique: it selects a combination that satisfies predefined
requirements rather than searching existing data for correlations or patterns.
Examples include assigning resources without conflicts, constructing schedules
where each required slot is filled once, and solving constraint puzzles such
as Sudoku. In Sudoku, a possible digit placement becomes a row choice, while
the rules about cells, rows, columns, and boxes become the requirements that
must each be satisfied exactly once.
"""

COLUMNS = {"A", "B", "C", "D"}

ROWS = {
    "Choice 1": {"A", "B"},
    "Choice 2": {"C", "D"},
    "Choice 3": {"A", "C"},
    "Choice 4": {"B", "D"},
}


def is_exact_cover(selected_rows: list[set[str]]) -> bool:
    """Return True when the selected rows cover every column exactly once."""

    # A list comprehension flattens all columns from the selected rows into one list.
    covered_columns = [column for row in selected_rows for column in row]

    # Check that every required column is present, then use the lengths to ensure
    # no column was covered more than once before duplicates were removed by set().
    return set(covered_columns) == COLUMNS and len(covered_columns) == len(COLUMNS)


if __name__ == "__main__":
    print("\n=== DEMONSTRATION: EXACT COVER ===")

    print(
        "Rows 1 & 2 cover AB + CD -> exact cover = "
        f"{is_exact_cover([ROWS['Choice 1'], ROWS['Choice 2']])}"
    )
    print(
        "Rows 1 & 3 cover AB + AC -> exact cover = "
        f"{is_exact_cover([ROWS['Choice 1'], ROWS['Choice 3']])}"
    )

    print()
