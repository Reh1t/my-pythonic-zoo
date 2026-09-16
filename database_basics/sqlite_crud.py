"""sqlite_crud.py

Transactional SQLite CRUD Execution Manager
--------------------------------------------

Demonstrates context-safe, parameterized SQLite operations using Python's
standard library without ORM dependencies.
"""

import sqlite3
from typing import Any, Self


class SQLiteManager:
    """Context-safe SQLite database CRUD execution manager.

    This manager encapsulates transactional operations against an SQLite database,
    ensuring connections are closed safely and queries are protected against SQL
    injection using parameter binding.
    """

    def __init__(self, db_path: str = ":memory:") -> None:
        """Initialize the database manager with an active connection.

        :param db_path: File path to the SQLite database or ``":memory:"``
            for an in-memory database.
        """
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row

    def __enter__(self) -> Self:
        """Enter the runtime context for managing the database connection."""
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: Any,
    ) -> None:
        """Exit the runtime context, ensuring the connection is closed."""
        self.close()

    def close(self) -> None:
        """Explicitly close the underlying database connection."""
        self.connection.close()

    def create_table(self) -> None:
        """Initialize sample schema with indexes.

        Creates the ``records`` table and an index on the ``name`` column if they
        do not already exist.
        """
        with self.connection:
            self.connection.execute(
                """
                CREATE TABLE IF NOT EXISTS records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    value REAL NOT NULL
                );
                """
            )
            self.connection.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_records_name
                ON records (name);
                """
            )

    def insert_record(self, name: str, value: float) -> int:
        """Insert a new record using parameterized queries.

        :param name: Descriptive label for the record.
        :param value: Numeric value associated with the record.
        :return: The generated primary key ID of the inserted record.
        :raises RuntimeError: If SQLite fails to return the inserted row ID.
        """
        query = "INSERT INTO records (name, value) VALUES (?, ?);"
        with self.connection:
            cursor = self.connection.execute(query, (name, value))
            if cursor.lastrowid is None:
                raise RuntimeError("Failed to retrieve inserted record ID.")
            return cursor.lastrowid

    def fetch_record_by_id(self, record_id: int) -> dict[str, Any] | None:
        """Retrieve a single record formatted as a dictionary.

        :param record_id: Primary key of the record to locate.
        :return: A dictionary representation of the record, or ``None`` if not found.
        """
        query = "SELECT id, name, value FROM records WHERE id = ?;"
        cursor = self.connection.execute(query, (record_id,))
        row = cursor.fetchone()
        if row is None:
            return None
        return dict(row)

    def update_record_value(self, record_id: int, new_value: float) -> bool:
        """Update an existing record safely within a transaction.

        :param record_id: Primary key of the record to modify.
        :param new_value: The replacement value for the record.
        :return: ``True`` if a row was updated, ``False`` if the ID was not found.
        """
        query = "UPDATE records SET value = ? WHERE id = ?;"
        with self.connection:
            cursor = self.connection.execute(query, (new_value, record_id))
            return cursor.rowcount > 0

    def delete_record(self, record_id: int) -> bool:
        """Remove a record by ID safely within a transaction.

        :param record_id: Primary key of the record to delete.
        :return: ``True`` if a row was removed, ``False`` if the ID was not found.
        """
        query = "DELETE FROM records WHERE id = ?;"
        with self.connection:
            cursor = self.connection.execute(query, (record_id,))
            return cursor.rowcount > 0


if __name__ == "__main__":
    # Example execution showcasing full CRUD lifecycle on an in-memory DB:
    # python -m database_basics.sqlite_crud
    with SQLiteManager(":memory:") as manager:
        manager.create_table()
        record_id = manager.insert_record("Sample Record", 42.0)
        print(f"Inserted record ID: {record_id}")

        record = manager.fetch_record_by_id(record_id)
        print(f"Fetched record: {record}")

        updated = manager.update_record_value(record_id, 84.0)
        print(f"Record updated: {updated}")

        record = manager.fetch_record_by_id(record_id)
        print(f"Updated record: {record}")

        deleted = manager.delete_record(record_id)
        print(f"Record deleted: {deleted}")

        record = manager.fetch_record_by_id(record_id)
        print(f"Record after deletion: {record}")
