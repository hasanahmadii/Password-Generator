"""
Database connection and initialization.

This module handles SQLite database connections,
initialization, and context management.
"""

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Generator

from config.settings import DATABASE_PATH
from database.models import get_create_table_statements


def init_database() -> None:
    """
    Initialize the database by creating all required tables.

    This function creates the database file if it doesn't exist
    and sets up all tables defined in models.py.
    """
    # Ensure the parent directory exists
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Create connection and tables
    conn = sqlite3.connect(DATABASE_PATH)
    conn.execute("PRAGMA foreign_keys = ON")  # Enable foreign key constraints

    try:
        cursor = conn.cursor()
        for statement in get_create_table_statements():
            cursor.execute(statement)
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise Exception(f"Failed to initialize database: {e}")
    finally:
        conn.close()


@contextmanager
def get_db_connection() -> Generator[sqlite3.Connection, None, None]:
    """
    Context manager for database connections.

    Yields:
        sqlite3.Connection: Database connection with row factory enabled

    Example:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")
            results = cursor.fetchall()
    """
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # Enable column access by name
    conn.execute("PRAGMA foreign_keys = ON")  # Enable foreign key constraints

    try:
        yield conn
    except sqlite3.Error as e:
        conn.rollback()
        raise Exception(f"Database error: {e}")
    finally:
        conn.close()


def get_connection() -> sqlite3.Connection:
    """
    Get a database connection (non-context manager version).

    Returns:
        sqlite3.Connection: Database connection

    Note:
        Caller is responsible for closing the connection.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def check_database_exists() -> bool:
    """
    Check if the database file exists.

    Returns:
        True if database file exists, False otherwise
    """
    return Path(DATABASE_PATH).exists()
