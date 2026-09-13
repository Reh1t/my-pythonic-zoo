# Context Managers

Context managers manage a lifecycle around a block of work. They define what
happens when that context is entered and what happens when it is exited, while
Python's `with` statement ensures those lifecycle methods are used at the
appropriate points.

The context manager does not necessarily own the work inside the block. Its
responsibility is the surrounding context: for example, acquiring and releasing
a resource, opening and closing a connection, acquiring and releasing a lock,
or temporarily changing and then restoring some state.

---

## More Than File Handling

Many Python developers first encounter context managers through
`with open(...)`,
but file handling is only one application of the protocol. The same lifecycle
pattern is useful for database connections and transactions, locks, temporary
files and directories, network connections, timers, redirected output, and
temporary changes to application state.

The important question is not whether some code could be placed inside `with`,
but whether it has a meaningful enter/exit lifecycle that should be managed
reliably.

---

## The Context Manager Protocol

A context manager used with the ordinary `with` statement implements two special
methods recognised by Python: `__enter__()` and `__exit__()`.

Python calls `__enter__()` before the managed block begins. If entering succeeds,
the block runs and Python later calls `__exit__()`. If the block raises an
exception, `__exit__()` is still called and receives the exception type,
exception object, and traceback.

If `__enter__()` itself fails, however, the managed block never begins and that
context manager's `__exit__()` is not called.

---

## Exceptions and Exit Handling

Calling `__exit__()` does not mean an exception is automatically hidden. By
default, an exception raised inside the managed block continues outward after
exit handling has run, allowing surrounding code to decide whether and how to
handle it.

A context manager can deliberately suppress an exception by returning `True`
from `__exit__()`. This should be intentional: suppressing unexpected exceptions
can hide bugs and make failures difficult to diagnose.

The guarantee also has a boundary. Python ensures that `__exit__()` is called
after the context has been entered successfully, but the exit handling itself
can still fail if its own code raises an exception.

---

## Using `with ... as ...`

`__enter__()` may return an object for use inside the managed block. When
`with ... as ...` is used, Python binds the value returned by `__enter__()` to
the name after `as`.

This is useful when the managed resource itself participates in the work, such
as a file, database connection, or another resource that exposes operations
while its context is active. A context manager does not have to return such an
object when the work is independent of the context being managed.

---

## What This Exhibit Demonstrates

`context_manager_example.py` shows successful context management, failure during
managed work, failure while entering, failure while exiting, deliberate
exception suppression, and using `with ... as ...` to work with a managed
resource.

Python's standard-library `contextlib` module also provides helpers for creating
context managers. In particular, `contextlib.contextmanager` uses generator
functions and `yield`, so that approach is deferred until generators have been
introduced elsewhere in Pythonic Thinking.

---

## Related Concepts

- **Names and objects** — the name after `as` is bound to the object returned by
  `__enter__()`. See the Names and Objects exhibit for Python's general name-binding model.
- **Generators** — generator functions and `yield` provide the foundation for
  `contextlib.contextmanager`, an alternative way to create context managers.
- **Asynchronous context managers** — asynchronous code can use `async with` and
  the related `__aenter__()` and `__aexit__()` protocol methods. These are outside the scope of this introductory exhibit.

---

| File | Last Updated | Maintainer |
| :--- | :---: | ---: |
| _pythonic_thinking/context_managers/README.md_ | _13 September 2026_ | _lizc-au_ |

---