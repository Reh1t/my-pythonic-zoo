"""
test_context_manager_example.py
"""

import pytest

from pythonic_thinking.context_managers.context_manager_example import (
    ManagedResource,
    ManagedTask,
    ManagedTaskFailsOnEnter,
    ManagedTaskFailsOnExit,
    ManagedTaskSuppressesError,
)


def test_managed_task_success(capsys):
    with ManagedTask():
        print("Test work")

    assert capsys.readouterr().out.splitlines() == [
        "Starting managed work",
        "Test work",
        "Exception details: None, None, None",
        "Finishing managed work",
    ]


def test_managed_task_exits_when_work_fails(capsys):
    with pytest.raises(RuntimeError, match="Something went wrong"):
        with ManagedTask():
            raise RuntimeError("Something went wrong")

    output = capsys.readouterr().out

    assert "Starting managed work" in output
    assert "RuntimeError" in output
    assert "Something went wrong" in output
    assert "Finishing managed work" in output


def test_managed_task_enter_failure_skips_block_and_exit(capsys):
    with pytest.raises(RuntimeError, match="Setup failed"):
        with ManagedTaskFailsOnEnter():
            print("This should not run")

    output = capsys.readouterr().out

    assert "Starting managed work" in output
    assert "This should not run" not in output
    assert "Finishing managed work" not in output


def test_managed_task_exit_failure_propagates(capsys):
    with pytest.raises(RuntimeError, match="Cleanup failed"):
        with ManagedTaskFailsOnExit():
            print("Test work")

    output = capsys.readouterr().out

    assert "Starting managed work" in output
    assert "Test work" in output
    assert "Finishing managed work" in output


def test_managed_task_can_suppress_error(capsys):
    with ManagedTaskSuppressesError():
        raise RuntimeError("Something went wrong")

    output = capsys.readouterr().out

    assert "RuntimeError" in output
    assert "Something went wrong" in output
    assert "Exception handled - finishing exit handling" in output


def test_managed_resource_is_bound_and_released(capsys):
    with ManagedResource() as resource:
        resource.use()

    assert capsys.readouterr().out.splitlines() == [
        "Acquiring managed resource",
        "Using managed resource",
        "Releasing managed resource",
    ]
