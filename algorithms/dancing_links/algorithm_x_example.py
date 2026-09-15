"""
algorithm_x_example.py

Demonstrate Knuth's Algorithm X using ordinary Python data structures.

The previous exact-cover example checked whether a supplied combination of rows
formed an exact cover. This example goes one step further: it searches for those
combinations automatically.

Without a search strategy, a program could generate possible combinations of
rows and test each one for an exact cover. That brute-force approach quickly
becomes expensive as the number of choices grows. Algorithm X avoids testing
every possible combination by using the exact-cover constraints to guide which
choices are worth exploring.

Algorithm X repeatedly chooses an uncovered column, tries each row that can
satisfy it, removes conflicting choices, and continues recursively. If a choice
leads to a dead end, the algorithm backtracks and tries another possibility.

Algorithm X does not define a new kind of problem: it is a method for solving
Exact Cover problems. The same real-world applications therefore apply,
including constraint-based scheduling and allocation, tiling problems, and
puzzles such as Sudoku. Dancing Links will later improve how Algorithm X
manages its changing search state without changing the problem being solved.

This version deliberately does not use Dancing Links. Its purpose is to make
the search and backtracking behaviour understandable before replacing ordinary
set operations with the specialised linked structure used by DLX.
"""

COLUMNS = {"A", "B", "C", "D"}

ROWS = {
    "Choice 1": {"A", "B"},
    "Choice 2": {"C", "D"},
    "Choice 3": {"A", "C"},
    "Choice 4": {"B", "D"},
}


def solve_exact_cover(
    columns: set[str],
    rows: dict[str, set[str]],
    solution: list[str],
) -> list[list[str]]:
    """Return all exact-cover solutions found by recursive Algorithm X."""

    # A recursive function needs a base case where it stops calling itself.
    # No remaining columns means every requirement has been covered successfully.
    if not columns:
        return [solution]

    # Choose one still-uncovered column to satisfy next. Using min() makes that
    # choice deterministic, so repeated runs explore the search in the same order.
    # Using next(iter(columns)) instead could vary the order between runs because
    # the columns are stored in a set.
    column = min(columns)

    # A list comprehension collects the names of rows that cover the chosen column.
    matching_rows = [name for name, covered in rows.items() if column in covered]

    # Start an empty list where this recursive call can collect any successful
    # solutions it discovers.
    solutions: list[list[str]] = []

    # Start Algorithm X branching - each row that can satisfy the chosen column
    # gets its own attempted search path.
    for row_name in matching_rows:
        selected_columns = rows[row_name]

        # Remove the columns satisfied by this row because those requirements
        # have now been covered on this search path.
        remaining_columns = columns - selected_columns

        # Keep only rows that share no columns with the selected row, because
        # any overlap would cover at least one requirement more than once.
        remaining_rows = {
            name: covered
            for name, covered in rows.items()
            if selected_columns.isdisjoint(covered)
        }

        # Iterable unpacking copies the current solution into a new list, then
        # appends this row name so each recursive branch gets its own search path.
        branch_solutions = solve_exact_cover(
            remaining_columns,
            remaining_rows,
            [*solution, row_name],
        )

        # use `.extend()` to add each solution to the solution list (not whole list)
        solutions.extend(branch_solutions)

    return solutions


if __name__ == "__main__":
    print("\n=== DEMONSTRATION: ALGORITHM X ===")

    solutions = solve_exact_cover(COLUMNS, ROWS, [])
    for solution in solutions:
        print(f"    Exact cover found: {solution}")

    print("\n=== SEARCH SUMMARY ===")
    print(
        """
    Start with requirements: A B C D

    Choose Row 1 (A B)
        remaining requirements: C D
        choose Row 2 (C D)
        -> exact cover found

    Backtrack and try another path:

    Choose Row 3 (A C)
        remaining requirements: B D
        choose Row 4 (B D)
        -> exact cover found

    Algorithm X explores choices, reduces the remaining problem,
    and backtracks to try alternatives.
    """
    )

    print()
