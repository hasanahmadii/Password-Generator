"""
Database package for the Password Generator application.
"""

from .db import init_database, get_db_connection, check_database_exists
from .crud import (
    create_user,
    get_user,
    get_all_users,
    update_user,
    delete_user,
    get_user_count,
    create_password,
    get_passwords_by_user,
    get_all_passwords,
    update_password,
    delete_password,
    get_password_count,
    search_users,
)

__all__ = [
    "init_database",
    "get_db_connection",
    "check_database_exists",
    "create_user",
    "get_user",
    "get_all_users",
    "update_user",
    "delete_user",
    "get_user_count",
    "create_password",
    "get_passwords_by_user",
    "get_all_passwords",
    "update_password",
    "delete_password",
    "get_password_count",
    "search_users",
]
