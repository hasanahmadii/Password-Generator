"""
CRUD operations for users and passwords.

This module provides Create, Read, Update, and Delete operations
for the users and passwords tables.
"""

import sqlite3
from datetime import datetime
from typing import Optional

from database.db import get_db_connection


# ============================================================================
# USER CRUD OPERATIONS
# ============================================================================

def create_user(first_name: str, last_name: str) -> int:
    """
    Create a new user in the database.

    Args:
        first_name: User's first name
        last_name: User's last name

    Returns:
        The ID of the newly created user

    Raises:
        Exception: If the database operation fails
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (first_name, last_name) VALUES (?, ?)",
            (first_name.strip(), last_name.strip())
        )
        conn.commit()
        return cursor.lastrowid


def get_user(user_id: int) -> Optional[dict]:
    """
    Retrieve a user by ID.

    Args:
        user_id: The ID of the user to retrieve

    Returns:
        Dictionary with user data, or None if not found
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, first_name, last_name, created_at FROM users WHERE id = ?",
            (user_id,)
        )
        row = cursor.fetchone()

        if row:
            return {
                "id": row["id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "created_at": row["created_at"]
            }
        return None


def get_all_users() -> list[dict]:
    """
    Retrieve all users from the database.

    Returns:
        List of dictionaries containing user data
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, first_name, last_name, created_at FROM users ORDER BY id DESC"
        )
        rows = cursor.fetchall()

        return [
            {
                "id": row["id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "created_at": row["created_at"]
            }
            for row in rows
        ]


def update_user(user_id: int, first_name: str, last_name: str) -> bool:
    """
    Update an existing user's information.

    Args:
        user_id: The ID of the user to update
        first_name: New first name
        last_name: New last name

    Returns:
        True if the user was updated, False if user not found

    Raises:
        Exception: If the database operation fails
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET first_name = ?, last_name = ? WHERE id = ?",
            (first_name.strip(), last_name.strip(), user_id)
        )
        conn.commit()
        return cursor.rowcount > 0


def delete_user(user_id: int) -> bool:
    """
    Delete a user and all their passwords (CASCADE).

    Args:
        user_id: The ID of the user to delete

    Returns:
        True if the user was deleted, False if user not found

    Raises:
        Exception: If the database operation fails
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        # Foreign key CASCADE will automatically delete associated passwords
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        return cursor.rowcount > 0


def get_user_count() -> int:
    """
    Get the total number of users.

    Returns:
        Total count of users
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM users")
        row = cursor.fetchone()
        return row["count"]


# ============================================================================
# PASSWORD CRUD OPERATIONS
# ============================================================================

def create_password(user_id: int, password: str, mode: str, length: int) -> int:
    """
    Create a new password entry for a user.

    Args:
        user_id: The ID of the user who owns this password
        password: The generated password
        mode: The password generation mode (PIN, TEXT, MIXED, STRONG)
        length: The length of the password

    Returns:
        The ID of the newly created password entry

    Raises:
        Exception: If the database operation fails
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO passwords (user_id, password, mode, length) VALUES (?, ?, ?, ?)",
            (user_id, password, mode, length)
        )
        conn.commit()
        return cursor.lastrowid


def get_passwords_by_user(user_id: int) -> list[dict]:
    """
    Retrieve all passwords for a specific user.

    Args:
        user_id: The ID of the user

    Returns:
        List of dictionaries containing password data
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, user_id, password, mode, length, created_at
            FROM passwords
            WHERE user_id = ?
            ORDER BY created_at DESC
            """,
            (user_id,)
        )
        rows = cursor.fetchall()

        return [
            {
                "id": row["id"],
                "user_id": row["user_id"],
                "password": row["password"],
                "mode": row["mode"],
                "length": row["length"],
                "created_at": row["created_at"]
            }
            for row in rows
        ]


def get_all_passwords() -> list[dict]:
    """
    Retrieve all passwords from the database with user information.

    Returns:
        List of dictionaries containing password and user data
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT
                p.id,
                p.user_id,
                p.password,
                p.mode,
                p.length,
                p.created_at,
                u.first_name,
                u.last_name
            FROM passwords p
            JOIN users u ON p.user_id = u.id
            ORDER BY p.created_at DESC
            """
        )
        rows = cursor.fetchall()

        return [
            {
                "id": row["id"],
                "user_id": row["user_id"],
                "password": row["password"],
                "mode": row["mode"],
                "length": row["length"],
                "created_at": row["created_at"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "full_name": f"{row['first_name']} {row['last_name']}"
            }
            for row in rows
        ]


def update_password(password_id: int, new_password: str) -> bool:
    """
    Update an existing password entry.

    Args:
        password_id: The ID of the password to update
        new_password: The new password value

    Returns:
        True if the password was updated, False if not found

    Raises:
        Exception: If the database operation fails
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE passwords SET password = ? WHERE id = ?",
            (new_password, password_id)
        )
        conn.commit()
        return cursor.rowcount > 0


def delete_password(password_id: int) -> bool:
    """
    Delete a password entry.

    Args:
        password_id: The ID of the password to delete

    Returns:
        True if the password was deleted, False if not found

    Raises:
        Exception: If the database operation fails
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM passwords WHERE id = ?", (password_id,))
        conn.commit()
        return cursor.rowcount > 0


def get_password_count() -> int:
    """
    Get the total number of passwords.

    Returns:
        Total count of passwords
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM passwords")
        row = cursor.fetchone()
        return row["count"]


def search_users(search_term: str) -> list[dict]:
    """
    Search for users by first name or last name.

    Args:
        search_term: The term to search for

    Returns:
        List of matching users
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        search_pattern = f"%{search_term}%"
        cursor.execute(
            """
            SELECT id, first_name, last_name, created_at
            FROM users
            WHERE first_name LIKE ? OR last_name LIKE ?
            ORDER BY id DESC
            """,
            (search_pattern, search_pattern)
        )
        rows = cursor.fetchall()

        return [
            {
                "id": row["id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "created_at": row["created_at"]
            }
            for row in rows
        ]
