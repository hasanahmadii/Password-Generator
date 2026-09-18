"""
Input validation functions for the Password Generator application.

This module contains all validation logic for user inputs,
password parameters, and data integrity checks.
"""

from typing import Tuple


def validate_name(name: str, field_name: str = "Name") -> Tuple[bool, str]:
    """
    Validate a name field (first name or last name).

    Args:
        name: The name string to validate
        field_name: The field name for error messages (default: "Name")

    Returns:
        Tuple of (is_valid: bool, error_message: str)
    """
    if not name:
        return False, f"{field_name} cannot be empty."

    if not name.strip():
        return False, f"{field_name} cannot contain only whitespace."

    if len(name.strip()) < 2:
        return False, f"{field_name} must be at least 2 characters long."

    if len(name.strip()) > 50:
        return False, f"{field_name} must be less than 50 characters."

    # Check if name contains only letters, spaces, hyphens, and apostrophes
    allowed_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ -'")
    if not all(char in allowed_chars for char in name):
        return False, f"{field_name} can only contain letters, spaces, hyphens, and apostrophes."

    return True, ""


def validate_password_length(length: int, min_length: int = 4, max_length: int = 64) -> Tuple[bool, str]:
    """
    Validate password length.

    Args:
        length: The password length to validate
        min_length: Minimum allowed length (default: 4)
        max_length: Maximum allowed length (default: 64)

    Returns:
        Tuple of (is_valid: bool, error_message: str)
    """
    if not isinstance(length, int):
        return False, "Password length must be an integer."

    if length < min_length:
        return False, f"Password length must be at least {min_length} characters."

    if length > max_length:
        return False, f"Password length must be at most {max_length} characters."

    return True, ""


def validate_password_mode(mode: str, valid_modes: list) -> Tuple[bool, str]:
    """
    Validate password generation mode.

    Args:
        mode: The password mode to validate
        valid_modes: List of valid mode strings

    Returns:
        Tuple of (is_valid: bool, error_message: str)
    """
    if not mode:
        return False, "Password mode cannot be empty."

    if mode not in valid_modes:
        return False, f"Invalid password mode. Must be one of: {', '.join(valid_modes)}"

    return True, ""


def validate_user_id(user_id: int) -> Tuple[bool, str]:
    """
    Validate user ID.

    Args:
        user_id: The user ID to validate

    Returns:
        Tuple of (is_valid: bool, error_message: str)
    """
    if not isinstance(user_id, int):
        return False, "User ID must be an integer."

    if user_id < 1:
        return False, "User ID must be a positive integer."

    return True, ""


def validate_password_id(password_id: int) -> Tuple[bool, str]:
    """
    Validate password ID.

    Args:
        password_id: The password ID to validate

    Returns:
        Tuple of (is_valid: bool, error_message: str)
    """
    if not isinstance(password_id, int):
        return False, "Password ID must be an integer."

    if password_id < 1:
        return False, "Password ID must be a positive integer."

    return True, ""


def get_password_strength(password: str) -> str:
    """
    Calculate password strength based on composition.

    Args:
        password: The password to evaluate

    Returns:
        Strength level: "Weak", "Medium", or "Strong"
    """
    if len(password) < 8:
        return "Weak"

    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(not c.isalnum() for c in password)

    complexity_score = sum([has_lower, has_upper, has_digit, has_symbol])

    if complexity_score >= 4 and len(password) >= 12:
        return "Strong"
    elif complexity_score >= 3 or (complexity_score >= 2 and len(password) >= 10):
        return "Medium"
    else:
        return "Weak"
