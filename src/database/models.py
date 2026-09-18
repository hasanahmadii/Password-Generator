"""
Database models and table definitions for the Password Generator application.

This module defines the database schema using raw SQL statements.
Tables: users and passwords with proper relationships.
"""

from typing import Final

# Users table schema
CREATE_USERS_TABLE: Final[str] = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""

# Passwords table schema with foreign key to users
CREATE_PASSWORDS_TABLE: Final[str] = """
CREATE TABLE IF NOT EXISTS passwords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    password TEXT NOT NULL,
    mode TEXT NOT NULL,
    length INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
)
"""

# Index for faster lookups
CREATE_USER_ID_INDEX: Final[str] = """
CREATE INDEX IF NOT EXISTS idx_passwords_user_id ON passwords(user_id)
"""

CREATE_MODE_INDEX: Final[str] = """
CREATE INDEX IF NOT EXISTS idx_passwords_mode ON passwords(mode)
"""


def get_create_table_statements() -> list[str]:
    """
    Get all CREATE TABLE and CREATE INDEX statements.

    Returns:
        List of SQL statements to initialize the database
    """
    return [
        CREATE_USERS_TABLE,
        CREATE_PASSWORDS_TABLE,
        CREATE_USER_ID_INDEX,
        CREATE_MODE_INDEX,
    ]
