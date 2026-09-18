"""
Configuration settings for the Password Generator application.

This module contains all configuration constants, database paths,
and application-wide settings.
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Database configuration
DATA_DIR = BASE_DIR / "data"
DATABASE_PATH = DATA_DIR / "app.db"

# Ensure data directory exists
DATA_DIR.mkdir(exist_ok=True)

# Password generation settings
PASSWORD_MODES = {
    "PIN": "digits",
    "TEXT": "letters",
    "MIXED": "letters_digits",
    "STRONG": "letters_digits_symbols"
}

# Password length constraints
MIN_PASSWORD_LENGTH = 4
MAX_PASSWORD_LENGTH = 64
DEFAULT_PIN_LENGTH = 6
DEFAULT_TEXT_LENGTH = 12
DEFAULT_MIXED_LENGTH = 16
DEFAULT_STRONG_LENGTH = 20

# UI Configuration
APP_TITLE = "🔐 Password Generator"
APP_ICON = "🔑"
VERSION = "1.0.0"

# Database table names
USERS_TABLE = "users"
PASSWORDS_TABLE = "passwords"
