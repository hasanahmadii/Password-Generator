"""
Unit tests for database CRUD operations.

Tests all Create, Read, Update, and Delete operations for users and passwords.
"""

import pytest
import sqlite3
from pathlib import Path
import tempfile
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database.db import init_database, get_db_connection
from src.database.crud import (
    create_user,
    get_user,
    get_all_users,
    update_user,
    delete_user,
    create_password,
    get_passwords_by_user,
    get_all_passwords,
    update_password,
    delete_password,
    search_users,
)
from src.config.settings import DATABASE_PATH


@pytest.fixture
def temp_db(monkeypatch):
    """Create a temporary database for testing."""
    # Create a temporary directory and database file
    temp_dir = tempfile.mkdtemp()
    temp_db_path = Path(temp_dir) / "test_app.db"

    # Monkeypatch the DATABASE_PATH
    monkeypatch.setattr("src.database.db.DATABASE_PATH", temp_db_path)
    monkeypatch.setattr("src.database.crud.get_db_connection",
                        lambda: get_test_connection(temp_db_path))

    # Initialize the database
    init_database()

    yield temp_db_path

    # Cleanup
    if temp_db_path.exists():
        temp_db_path.unlink()


def get_test_connection(db_path):
    """Get a connection to the test database."""
    from contextlib import contextmanager

    @contextmanager
    def connection():
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        try:
            yield conn
        finally:
            conn.close()

    return connection()


class TestUserCRUD:
    """Test user CRUD operations."""

    def test_create_user(self, temp_db):
        """Test creating a new user."""
        user_id = create_user("John", "Doe")
        assert user_id > 0

    def test_get_user(self, temp_db):
        """Test retrieving a user by ID."""
        user_id = create_user("Jane", "Smith")
        user = get_user(user_id)

        assert user is not None
        assert user["id"] == user_id
        assert user["first_name"] == "Jane"
        assert user["last_name"] == "Smith"

    def test_get_nonexistent_user(self, temp_db):
        """Test retrieving a user that doesn't exist."""
        user = get_user(99999)
        assert user is None

    def test_get_all_users(self, temp_db):
        """Test retrieving all users."""
        create_user("Alice", "Johnson")
        create_user("Bob", "Williams")
        create_user("Charlie", "Brown")

        users = get_all_users()
        assert len(users) == 3

    def test_update_user(self, temp_db):
        """Test updating a user."""
        user_id = create_user("Old", "Name")
        success = update_user(user_id, "New", "Name")

        assert success is True

        user = get_user(user_id)
        assert user["first_name"] == "New"
        assert user["last_name"] == "Name"

    def test_update_nonexistent_user(self, temp_db):
        """Test updating a user that doesn't exist."""
        success = update_user(99999, "New", "Name")
        assert success is False

    def test_delete_user(self, temp_db):
        """Test deleting a user."""
        user_id = create_user("Delete", "Me")
        success = delete_user(user_id)

        assert success is True

        user = get_user(user_id)
        assert user is None

    def test_delete_nonexistent_user(self, temp_db):
        """Test deleting a user that doesn't exist."""
        success = delete_user(99999)
        assert success is False

    def test_search_users(self, temp_db):
        """Test searching for users."""
        create_user("Alice", "Anderson")
        create_user("Bob", "Smith")
        create_user("Alice", "Brown")

        results = search_users("Alice")
        assert len(results) == 2

        results = search_users("Smith")
        assert len(results) == 1


class TestPasswordCRUD:
    """Test password CRUD operations."""

    def test_create_password(self, temp_db):
        """Test creating a new password entry."""
        user_id = create_user("Test", "User")
        password_id = create_password(user_id, "TestPass123!", "MIXED", 12)

        assert password_id > 0

    def test_get_passwords_by_user(self, temp_db):
        """Test retrieving passwords for a specific user."""
        user_id = create_user("Test", "User")

        create_password(user_id, "Pass1", "PIN", 6)
        create_password(user_id, "Pass2", "TEXT", 12)
        create_password(user_id, "Pass3", "STRONG", 20)

        passwords = get_passwords_by_user(user_id)
        assert len(passwords) == 3

    def test_get_all_passwords(self, temp_db):
        """Test retrieving all passwords."""
        user1_id = create_user("User", "One")
        user2_id = create_user("User", "Two")

        create_password(user1_id, "Pass1", "PIN", 6)
        create_password(user2_id, "Pass2", "TEXT", 12)

        passwords = get_all_passwords()
        assert len(passwords) == 2

        # Check that user information is included
        assert "full_name" in passwords[0]

    def test_update_password(self, temp_db):
        """Test updating a password."""
        user_id = create_user("Test", "User")
        password_id = create_password(user_id, "OldPass", "TEXT", 8)

        success = update_password(password_id, "NewPass")
        assert success is True

    def test_delete_password(self, temp_db):
        """Test deleting a password."""
        user_id = create_user("Test", "User")
        password_id = create_password(user_id, "DeleteMe", "PIN", 6)

        success = delete_password(password_id)
        assert success is True

    def test_cascade_delete(self, temp_db):
        """Test that deleting a user cascades to their passwords."""
        user_id = create_user("Test", "User")

        create_password(user_id, "Pass1", "PIN", 6)
        create_password(user_id, "Pass2", "TEXT", 12)

        passwords_before = get_passwords_by_user(user_id)
        assert len(passwords_before) == 2

        # Delete the user
        delete_user(user_id)

        # Passwords should be gone
        passwords_after = get_passwords_by_user(user_id)
        assert len(passwords_after) == 0


class TestDataIntegrity:
    """Test data integrity and edge cases."""

    def test_whitespace_handling(self, temp_db):
        """Test that whitespace is properly trimmed."""
        user_id = create_user("  John  ", "  Doe  ")
        user = get_user(user_id)

        assert user["first_name"] == "John"
        assert user["last_name"] == "Doe"

    def test_special_characters_in_password(self, temp_db):
        """Test passwords with special characters."""
        user_id = create_user("Test", "User")
        special_password = "P@ssw0rd!#$%^&*()"

        password_id = create_password(user_id, special_password, "STRONG", len(special_password))

        passwords = get_passwords_by_user(user_id)
        assert passwords[0]["password"] == special_password

    def test_empty_database(self, temp_db):
        """Test operations on an empty database."""
        users = get_all_users()
        assert len(users) == 0

        passwords = get_all_passwords()
        assert len(passwords) == 0
