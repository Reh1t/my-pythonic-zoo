"""
context_manager_example.py

Demonstrate the context manager protocol behind Python's `with` statement.

A context manager controls a lifecycle around a block of work: something
happens when the context is entered, the managed work runs, and something
happens when the context is exited. The work does not have to belong to the
context manager itself.

Python's `with` statement recognises objects that implement the context manager
protocol. It calls `__enter__()` before running the managed block and
`__exit__()` afterwards. These special method names are defined by Python;
the `ManagedTask` class name used in this example has no special meaning.

`__exit__()` is called even when the managed work raises an exception. Python
passes information about that exception to `__exit__()`, allowing the context
manager to perform appropriate cleanup or other exit behaviour. A context
manager can suppress an exception by returning `True` from `__exit__()`, but
silently suppressing unexpected errors can hide bugs and should be deliberate.

Context managers are useful when code has a genuine enter/exit lifecycle, such
as acquiring and releasing a resource or temporarily changing and then
restoring some state. They are not intended as general-purpose safety wrappers
around arbitrary code.

Files are a familiar use of context managers, but file handling is only one
application of the protocol. Other common uses include database connections
and transactions, thread and process locks, temporary files and directories,
network connections, timers, redirected output, and temporarily changing then
restoring application state.
"""

# `__exit__()` receives a traceback object when managed work raises an exception.
# `TracebackType` lets the type annotations describe that standard Python object.
from types import TracebackType


class ManagedTask:
    """Demonstrate the enter and exit methods of the context manager protocol."""

    def __enter__(self) -> None:
        """Called automatically by Python when entering the `with` block."""
        # This setup happens before any code inside the managed block runs.
        # If it fails, the block does not run and `__exit__()` is not called.
        print("Starting managed work")

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """
        Called automatically by Python when leaving the `with` block.
        Python supplies details of any exception raised inside the block.
        """
        # Python supplies the exception type, exception object, and traceback.
        # If the managed block succeeds, all three values are `None`.
        print(f"Exception details: {exc_type}, {exc_value}, {traceback}")

        # Because this method does not return `True`, any exception continues outward.
        print("Finishing managed work")


class ManagedTaskFailsOnEnter:
    """Demonstrate what happens when entering the context fails."""

    def __enter__(self) -> None:
        """Called automatically by Python when entering the `with` block."""
        print("Starting managed work")
        raise RuntimeError("Setup failed")

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Called automatically by Python when leaving the `with` block."""
        print("Finishing managed work")


class ManagedTaskFailsOnExit:
    """Demonstrate what happens when leaving the context fails."""

    def __enter__(self) -> None:
        """Called automatically by Python when entering the `with` block."""
        print("Starting managed work")

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Called automatically by Python when leaving the `with` block."""
        print("Finishing managed work")
        raise RuntimeError("Cleanup failed")


class ManagedTaskSuppressesError:
    """Demonstrate deliberate exception suppression during exit handling."""

    def __enter__(self) -> None:
        """Called automatically by Python when entering the `with` block."""
        print("Starting managed work")

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool:
        """Suppress an exception by returning `True` from exit handling."""
        print(f"Exception details: {exc_type}, {exc_value}, {traceback}")
        print("Exception handled - finishing exit handling")
        return True


class ManagedResource:
    """Demonstrate returning a managed object from `__enter__()`."""

    def __enter__(self) -> "ManagedResource":
        """Return this managed object for use after `as`."""
        print("Acquiring managed resource")
        return self

    def use(self) -> None:
        """Perform work through the managed resource."""
        print("Using managed resource")

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Release the managed resource when leaving the `with` block."""
        print("Releasing managed resource")


def do_work_successfully() -> None:
    # This is ordinary application code, not part of the context manager protocol.
    print("Managed task completed successfully")


def do_work_with_error() -> None:
    # This is also ordinary application code, not part of the context manager protocol.
    print("Managed task encountered an error")
    raise RuntimeError("Something went wrong")


print("\n=== DEMONSTRATION 1: SUCCESSFUL CONTEXT ===")
with ManagedTask():
    do_work_successfully()

# Catch propagated errors in the following demonstrations so this teaching
# script can continue. Real application code should catch an exception only
# when it can handle that failure meaningfully.

print("\n=== DEMONSTRATION 2: WORK FAILS ===")

# This demonstrates what happens when the managed work itself fails -
# → context manager gets the error and performs exit handling
# → context manager does not suppress it
# → caller receives it and decides what to do
try:
    with ManagedTask():
        do_work_with_error()
except RuntimeError as error:
    print(f"Caller caught propagated error: {error}")

print("\n=== DEMONSTRATION 3: ENTER FAILS ===")

# This demonstrates what happens when entering the context itself fails -
# → the managed block does not run
# → __exit__() isn't involved at all
# → the exception propagates directly to the caller, which decides what to do
try:
    with ManagedTaskFailsOnEnter():
        do_work_successfully()
except RuntimeError as error:
    print(f"Caller caught enter error: {error}")

print("\n=== DEMONSTRATION 4: EXIT FAILS ===")

# This demonstrates what happens when exit handling itself fails -
# → the managed block has already completed successfully
# → __exit__() itself raises a new exception
# → that exception propagates to the caller, which decides what to do
try:
    with ManagedTaskFailsOnExit():
        do_work_successfully()
except RuntimeError as error:
    print(f"Caller caught exit error: {error}")

print("\n=== DEMONSTRATION 5: EXCEPTION SUPPRESSED ===")

# Returning `True` from __exit__() tells Python that the exception has been
# handled, so it does not propagate to the caller.
with ManagedTaskSuppressesError():
    do_work_with_error()

print("Program continues because the context manager suppressed the error")

print("\n=== DEMONSTRATION 6: USING `WITH ... AS ...` ===")

# __enter__() returns the managed object, `as` binds it to `resource`,
# and __exit__() performs the resource's release handling.
with ManagedResource() as resource:
    resource.use()

print()
