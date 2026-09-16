"""
test_sqlite_crud.py

Unit tests for the transactional SQLite CRUD execution manager.
"""

import sqlite3
from collections.abc import Generator

import pytest

from database_basics.sqlite_crud import SQLiteManager


@pytest.fixture
def manager() -> Generator[SQLiteManager, None, None]:
    """Fixture providing an initialized in-memory SQLite manager."""
    db = SQLiteManager(":memory:")
    db.create_table()
    yield db
    db.close()


def test_insert_and_fetch_record(manager: SQLiteManager) -> None:
    """Inserting a record should return an ID and allow dictionary retrieval."""
    expected_value = 1.50
    record_id = manager.insert_record("Apple", expected_value)
    assert record_id > 0

    record = manager.fetch_record_by_id(record_id)
    assert record is not None
    assert record["id"] == record_id
    assert record["name"] == "Apple"
    assert record["value"] == expected_value


def test_fetch_nonexistent_record_returns_none(manager: SQLiteManager) -> None:
    """Fetching an ID that does not exist should return None."""
    non_existent_id = 9999
    record = manager.fetch_record_by_id(non_existent_id)
    assert record is None


def test_update_record_value_success(manager: SQLiteManager) -> None:
    """Updating an existing record should modify its value and return True."""
    initial_value = 0.80
    new_value = 1.20
    record_id = manager.insert_record("Banana", initial_value)

    success = manager.update_record_value(record_id, new_value)
    assert success is True

    record = manager.fetch_record_by_id(record_id)
    assert record is not None
    assert record["value"] == new_value


def test_update_nonexistent_record_returns_false(manager: SQLiteManager) -> None:
    """Updating a non-existent ID should return False."""
    non_existent_id = 9999
    success = manager.update_record_value(non_existent_id, 5.00)
    assert success is False


def test_delete_record_success(manager: SQLiteManager) -> None:
    """Deleting an existing record should remove it and return True."""
    record_id = manager.insert_record("Orange", 2.00)

    deleted = manager.delete_record(record_id)
    assert deleted is True

    record = manager.fetch_record_by_id(record_id)
    assert record is None


def test_delete_nonexistent_record_returns_false(manager: SQLiteManager) -> None:
    """Deleting a non-existent ID should return False."""
    non_existent_id = 9999
    deleted = manager.delete_record(non_existent_id)
    assert deleted is False


def test_context_manager_lifecycle() -> None:
    """Manager should support context protocol and close connection on exit."""
    with SQLiteManager(":memory:") as db:
        db.create_table()
        record_id = db.insert_record("Pear", 3.10)
        assert record_id > 0

    # Operations after exit should fail because connection is closed
    with pytest.raises(sqlite3.ProgrammingError):
        db.fetch_record_by_id(record_id)
