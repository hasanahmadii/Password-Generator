"""
Password generation logic with multiple modes.

This module provides functions to generate passwords in different modes:
PIN (digits only), TEXT (letters only), MIXED (letters + digits),
and STRONG (letters + digits + symbols).
"""

import random
import string
from typing import Literal

PasswordMode = Literal["PIN", "TEXT", "MIXED", "STRONG"]


def generate_pin(length: int = 6) -> str:
    """
    Generate a PIN (digits only).

    Args:
        length: Length of the PIN (default: 6)

    Returns:
        Generated PIN as a string
    """
    return ''.join(random.choices(string.digits, k=length))


def generate_text(length: int = 12) -> str:
    """
    Generate a text-only password (letters only).

    Args:
        length: Length of the password (default: 12)

    Returns:
        Generated password with letters only
    """
    characters = string.ascii_letters
    return ''.join(random.choices(characters, k=length))


def generate_mixed(length: int = 16) -> str:
    """
    Generate a mixed password (letters + digits).

    Args:
        length: Length of the password (default: 16)

    Returns:
        Generated password with letters and digits
    """
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))


def generate_strong(length: int = 20) -> str:
    """
    Generate a strong password (letters + digits + symbols).

    Ensures the password contains at least one character from each category:
    - Lowercase letter
    - Uppercase letter
    - Digit
    - Symbol

    Args:
        length: Length of the password (default: 20)

    Returns:
        Generated strong password
    """
    if length < 4:
        # If length is too small, just generate random characters
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choices(characters, k=length))

    # Ensure at least one character from each category
    password_chars = [
        random.choice(string.ascii_lowercase),
        random.choice(string.ascii_uppercase),
        random.choice(string.digits),
        random.choice(string.punctuation),
    ]

    # Fill the rest with random characters from all categories
    all_characters = string.ascii_letters + string.digits + string.punctuation
    remaining_length = length - 4
    password_chars.extend(random.choices(all_characters, k=remaining_length))

    # Shuffle to avoid predictable patterns
    random.shuffle(password_chars)

    return ''.join(password_chars)


def generate_password(mode: PasswordMode, length: int) -> str:
    """
    Generate a password based on the specified mode and length.

    Args:
        mode: Password generation mode ("PIN", "TEXT", "MIXED", "STRONG")
        length: Desired password length

    Returns:
        Generated password string

    Raises:
        ValueError: If an invalid mode is provided
    """
    mode_functions = {
        "PIN": generate_pin,
        "TEXT": generate_text,
        "MIXED": generate_mixed,
        "STRONG": generate_strong,
    }

    if mode not in mode_functions:
        raise ValueError(f"Invalid password mode: {mode}. Must be one of {list(mode_functions.keys())}")

    return mode_functions[mode](length)
