# Password Generator - Complete API Documentation

**Version:** 1.0.0  
**Last Updated:** September 18, 2026

This document provides comprehensive documentation for all modules, classes, and functions in the Password Generator application.

---

## Table of Contents

1. [Overview](#overview)
2. [Core Modules](#core-modules)
   - [generator.py](#generatorpy)
   - [validators.py](#validatorspy)
3. [Database Modules](#database-modules)
   - [db.py](#dbpy)
   - [models.py](#modelspy)
   - [crud.py](#crudpy)
4. [Configuration](#configuration)
   - [settings.py](#settingspy)
5. [UI Modules](#ui-modules)
   - [components.py](#componentspy)
   - [pages.py](#pagespy)
6. [Main Application](#main-application)
   - [main.py](#mainpy)
   - [run.py](#runpy)
7. [Testing](#testing)
8. [Usage Examples](#usage-examples)

---

## Overview

The Password Generator is a desktop application built with Python and Streamlit. It provides multiple password generation modes and stores them in a local SQLite database with full user management capabilities.

### Key Features
- 4 password generation modes (PIN, TEXT, MIXED, STRONG)
- User management with CRUD operations
- Password storage and management
- Strength evaluation
- CSV export functionality
- Modern, responsive UI

---

## Core Modules

### generator.py

Location: `src/core/generator.py`

This module provides all password generation functionality with multiple modes.

#### Type Definitions

```python
PasswordMode = Literal["PIN", "TEXT", "MIXED", "STRONG"]
```

#### Functions

##### `generate_pin(length: int = 6) -> str`

Generate a PIN consisting of digits only.

**Parameters:**
- `length` (int, optional): Length of the PIN. Default is 6.

**Returns:**
- `str`: Generated PIN as a string

**Example:**
```python
pin = generate_pin(8)
# Output: "48572916"
```

---

##### `generate_text(length: int = 12) -> str`

Generate a text-only password with letters only.

**Parameters:**
- `length` (int, optional): Length of the password. Default is 12.

**Returns:**
- `str`: Generated password containing only letters

**Example:**
```python
text = generate_text(10)
# Output: "AbCdEfGhIj"
```

---

##### `generate_mixed(length: int = 16) -> str`

Generate a mixed password with letters and digits.

**Parameters:**
- `length` (int, optional): Length of the password. Default is 16.

**Returns:**
- `str`: Generated password with letters and digits

**Example:**
```python
mixed = generate_mixed(12)
# Output: "Ab3Cd5Ef7Gh9"
```

---

##### `generate_strong(length: int = 20) -> str`

Generate a strong password with letters, digits, and symbols.

This function guarantees at least one character from each category:
- Lowercase letter
- Uppercase letter
- Digit
- Symbol

**Parameters:**
- `length` (int, optional): Length of the password. Default is 20. Minimum recommended is 4.

**Returns:**
- `str`: Generated strong password

**Example:**
```python
strong = generate_strong(16)
# Output: "A@3bC#5dE$7fG%9h"
```

**Notes:**
- For lengths < 4, the guarantee of all character types may not apply
- Characters are shuffled to avoid predictable patterns

---

##### `generate_password(mode: PasswordMode, length: int) -> str`

Main password generation function that delegates to specific generators based on mode.

**Parameters:**
- `mode` (PasswordMode): One of "PIN", "TEXT", "MIXED", or "STRONG"
- `length` (int): Desired password length

**Returns:**
- `str`: Generated password

**Raises:**
- `ValueError`: If an invalid mode is provided

**Example:**
```python
password = generate_password("STRONG", 20)
# Output depends on random generation
```

---

### validators.py

Location: `src/core/validators.py`

This module contains all input validation functions.

#### Functions

##### `validate_name(name: str, field_name: str = "Name") -> Tuple[bool, str]`

Validate a name field (first name or last name).

**Parameters:**
- `name` (str): The name string to validate
- `field_name` (str, optional): Field name for error messages. Default is "Name".

**Returns:**
- `Tuple[bool, str]`: (is_valid, error_message)
  - `is_valid`: True if validation passes, False otherwise
  - `error_message`: Empty string if valid, error description if invalid

**Validation Rules:**
- Cannot be empty
- Cannot contain only whitespace
- Must be at least 2 characters long
- Must be less than 50 characters
- Can only contain letters, spaces, hyphens, and apostrophes

**Example:**
```python
is_valid, error = validate_name("John", "First Name")
# Returns: (True, "")

is_valid, error = validate_name("J", "First Name")
# Returns: (False, "First Name must be at least 2 characters long.")
```

---

##### `validate_password_length(length: int, min_length: int = 4, max_length: int = 64) -> Tuple[bool, str]`

Validate password length.

**Parameters:**
- `length` (int): The password length to validate
- `min_length` (int, optional): Minimum allowed length. Default is 4.
- `max_length` (int, optional): Maximum allowed length. Default is 64.

**Returns:**
- `Tuple[bool, str]`: (is_valid, error_message)

**Example:**
```python
is_valid, error = validate_password_length(16)
# Returns: (True, "")

is_valid, error = validate_password_length(100)
# Returns: (False, "Password length must be at most 64 characters.")
```

---

##### `validate_password_mode(mode: str, valid_modes: list) -> Tuple[bool, str]`

Validate password generation mode.

**Parameters:**
- `mode` (str): The password mode to validate
- `valid_modes` (list): List of valid mode strings

**Returns:**
- `Tuple[bool, str]`: (is_valid, error_message)

**Example:**
```python
is_valid, error = validate_password_mode("STRONG", ["PIN", "TEXT", "MIXED", "STRONG"])
# Returns: (True, "")
```

---

##### `validate_user_id(user_id: int) -> Tuple[bool, str]`

Validate user ID.

**Parameters:**
- `user_id` (int): The user ID to validate

**Returns:**
- `Tuple[bool, str]`: (is_valid, error_message)

**Validation Rules:**
- Must be an integer
- Must be a positive integer (>= 1)

---

##### `validate_password_id(password_id: int) -> Tuple[bool, str]`

Validate password ID.

**Parameters:**
- `password_id` (int): The password ID to validate

**Returns:**
- `Tuple[bool, str]`: (is_valid, error_message)

**Validation Rules:**
- Must be an integer
- Must be a positive integer (>= 1)

---

##### `get_password_strength(password: str) -> str`

Calculate password strength based on composition.

**Parameters:**
- `password` (str): The password to evaluate

**Returns:**
- `str`: Strength level - "Weak", "Medium", or "Strong"

**Strength Criteria:**
- **Strong**: Length >= 12 AND has all 4 character types (lower, upper, digit, symbol)
- **Medium**: Has 3+ character types OR (2+ types AND length >= 10)
- **Weak**: Everything else, or length < 8

**Example:**
```python
strength = get_password_strength("Pass123!")
# Returns: "Medium"

strength = get_password_strength("P@ssw0rd!2024")
# Returns: "Strong"
```

---

## Database Modules

### db.py

Location: `src/database/db.py`

Handles SQLite database connections and initialization.

#### Functions

##### `init_database() -> None`

Initialize the database by creating all required tables.

Creates the database file if it doesn't exist and sets up all tables defined in models.py. Enables foreign key constraints.

**Raises:**
- `Exception`: If database initialization fails

**Example:**
```python
init_database()
```

---

##### `get_db_connection() -> Generator[sqlite3.Connection, None, None]`

Context manager for database connections.

**Yields:**
- `sqlite3.Connection`: Database connection with row factory enabled

**Example:**
```python
with get_db_connection() as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
```

**Features:**
- Automatic connection cleanup
- Row factory enabled (access columns by name)
- Foreign key constraints enabled
- Automatic rollback on error

---

##### `get_connection() -> sqlite3.Connection`

Get a database connection (non-context manager version).

**Returns:**
- `sqlite3.Connection`: Database connection

**Note:** Caller is responsible for closing the connection.

---

##### `check_database_exists() -> bool`

Check if the database file exists.

**Returns:**
- `bool`: True if database file exists, False otherwise

---

### models.py

Location: `src/database/models.py`

Defines the database schema using raw SQL statements.

#### SQL Schemas

##### Users Table

```sql
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

##### Passwords Table

```sql
CREATE TABLE IF NOT EXISTS passwords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    password TEXT NOT NULL,
    mode TEXT NOT NULL,
    length INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
)
```

##### Indexes

- `idx_passwords_user_id`: Index on passwords.user_id for faster lookups
- `idx_passwords_mode`: Index on passwords.mode for filtering by mode

#### Functions

##### `get_create_table_statements() -> list[str]`

Get all CREATE TABLE and CREATE INDEX statements.

**Returns:**
- `list[str]`: List of SQL statements to initialize the database

---

### crud.py

Location: `src/database/crud.py`

Provides Create, Read, Update, and Delete operations for users and passwords.

#### User CRUD Operations

##### `create_user(first_name: str, last_name: str) -> int`

Create a new user in the database.

**Parameters:**
- `first_name` (str): User's first name
- `last_name` (str): User's last name

**Returns:**
- `int`: The ID of the newly created user

**Raises:**
- `Exception`: If the database operation fails

**Example:**
```python
user_id = create_user("John", "Doe")
# Returns: 1
```

---

##### `get_user(user_id: int) -> Optional[dict]`

Retrieve a user by ID.

**Parameters:**
- `user_id` (int): The ID of the user to retrieve

**Returns:**
- `Optional[dict]`: Dictionary with user data, or None if not found
  - `id`: User ID
  - `first_name`: User's first name
  - `last_name`: User's last name
  - `created_at`: Timestamp of creation

**Example:**
```python
user = get_user(1)
# Returns: {"id": 1, "first_name": "John", "last_name": "Doe", "created_at": "2026-09-18 ..."}
```

---

##### `get_all_users() -> list[dict]`

Retrieve all users from the database.

**Returns:**
- `list[dict]`: List of dictionaries containing user data, ordered by ID descending

**Example:**
```python
users = get_all_users()
# Returns: [{"id": 2, ...}, {"id": 1, ...}]
```

---

##### `update_user(user_id: int, first_name: str, last_name: str) -> bool`

Update an existing user's information.

**Parameters:**
- `user_id` (int): The ID of the user to update
- `first_name` (str): New first name
- `last_name` (str): New last name

**Returns:**
- `bool`: True if the user was updated, False if user not found

**Raises:**
- `Exception`: If the database operation fails

---

##### `delete_user(user_id: int) -> bool`

Delete a user and all their passwords (CASCADE).

**Parameters:**
- `user_id` (int): The ID of the user to delete

**Returns:**
- `bool`: True if the user was deleted, False if user not found

**Raises:**
- `Exception`: If the database operation fails

**Note:** This will also delete all passwords associated with this user.

---

##### `get_user_count() -> int`

Get the total number of users.

**Returns:**
- `int`: Total count of users

---

##### `search_users(search_term: str) -> list[dict]`

Search for users by first name or last name.

**Parameters:**
- `search_term` (str): The term to search for

**Returns:**
- `list[dict]`: List of matching users

**Example:**
```python
results = search_users("John")
# Returns all users with "John" in first or last name
```

---

#### Password CRUD Operations

##### `create_password(user_id: int, password: str, mode: str, length: int) -> int`

Create a new password entry for a user.

**Parameters:**
- `user_id` (int): The ID of the user who owns this password
- `password` (str): The generated password
- `mode` (str): The password generation mode (PIN, TEXT, MIXED, STRONG)
- `length` (int): The length of the password

**Returns:**
- `int`: The ID of the newly created password entry

**Raises:**
- `Exception`: If the database operation fails

---

##### `get_passwords_by_user(user_id: int) -> list[dict]`

Retrieve all passwords for a specific user.

**Parameters:**
- `user_id` (int): The ID of the user

**Returns:**
- `list[dict]`: List of dictionaries containing password data

---

##### `get_all_passwords() -> list[dict]`

Retrieve all passwords from the database with user information.

**Returns:**
- `list[dict]`: List of dictionaries containing password and user data
  - Includes `full_name` field combining first and last name

**Example:**
```python
passwords = get_all_passwords()
# Returns: [{"id": 1, "password": "...", "full_name": "John Doe", ...}]
```

---

##### `update_password(password_id: int, new_password: str) -> bool`

Update an existing password entry.

**Parameters:**
- `password_id` (int): The ID of the password to update
- `new_password` (str): The new password value

**Returns:**
- `bool`: True if updated, False if not found

---

##### `delete_password(password_id: int) -> bool`

Delete a password entry.

**Parameters:**
- `password_id` (int): The ID of the password to delete

**Returns:**
- `bool`: True if deleted, False if not found

---

##### `get_password_count() -> int`

Get the total number of passwords.

**Returns:**
- `int`: Total count of passwords

---

## Configuration

### settings.py

Location: `src/config/settings.py`

Contains all configuration constants and application-wide settings.

#### Path Configuration

```python
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
DATABASE_PATH = DATA_DIR / "app.db"
```

#### Password Configuration

```python
PASSWORD_MODES = {
    "PIN": "digits",
    "TEXT": "letters",
    "MIXED": "letters_digits",
    "STRONG": "letters_digits_symbols"
}

MIN_PASSWORD_LENGTH = 4
MAX_PASSWORD_LENGTH = 64
DEFAULT_PIN_LENGTH = 6
DEFAULT_TEXT_LENGTH = 12
DEFAULT_MIXED_LENGTH = 16
DEFAULT_STRONG_LENGTH = 20
```

#### UI Configuration

```python
APP_TITLE = "🔐 Password Generator"
APP_ICON = "🔑"
VERSION = "1.0.0"
```

#### Database Configuration

```python
USERS_TABLE = "users"
PASSWORDS_TABLE = "passwords"
```

---

## UI Modules

### components.py

Location: `src/ui/components.py`

Contains reusable UI components for the Streamlit application.

#### Functions

##### `render_page_header(title: str, icon: str = "🔐", subtitle: Optional[str] = None) -> None`

Render a consistent page header.

**Parameters:**
- `title` (str): The page title
- `icon` (str, optional): Icon emoji. Default is "🔐".
- `subtitle` (Optional[str]): Optional subtitle text

---

##### `render_info_box(message: str, type: str = "info") -> None`

Render an info/warning/error box.

**Parameters:**
- `message` (str): The message to display
- `type` (str): Type of box - "info", "success", "warning", or "error"

---

##### `render_strength_indicator(strength: str) -> None`

Render a password strength indicator with color coding.

**Parameters:**
- `strength` (str): Strength level ("Weak", "Medium", "Strong")

**Color Mapping:**
- Weak: Red (🔴)
- Medium: Yellow (🟡)
- Strong: Green (🟢)

---

##### `render_password_display(password: str, strength: str) -> None`

Render the generated password with a copy button and strength indicator.

**Parameters:**
- `password` (str): The password to display
- `strength` (str): Password strength level

---

##### `render_stats_card(label: str, value: int, icon: str = "📊") -> None`

Render a statistics card with gradient background.

**Parameters:**
- `label` (str): The stat label
- `value` (int): The stat value
- `icon` (str): Icon emoji

---

##### `render_empty_state(message: str, icon: str = "📭") -> None`

Render an empty state message.

**Parameters:**
- `message` (str): The message to display
- `icon` (str): Icon emoji

---

##### `render_user_card(user: dict, show_actions: bool = True) -> None`

Render a user information card.

**Parameters:**
- `user` (dict): User dictionary with id, first_name, last_name, created_at
- `show_actions` (bool): Whether to show action buttons

---

##### `render_password_card(password_entry: dict) -> None`

Render a password entry card with mode icon and details.

**Parameters:**
- `password_entry` (dict): Password dictionary with all fields

**Mode Icons:**
- PIN: 🔢
- TEXT: 🔤
- MIXED: 🔀
- STRONG: 💪

---

##### `render_footer() -> None`

Render the application footer.

---

### pages.py

Location: `src/ui/pages.py`

Contains the three main page functions for the Streamlit application.

#### Functions

##### `page_generate_password() -> None`

Render the password generation page.

**Features:**
- User name input (first and last name)
- Password mode selection
- Password length slider with mode-specific defaults
- Generate button with validation
- Password display with strength indicator
- Save to database functionality

---

##### `page_manage_users() -> None`

Render the user management page.

**Features:**
- Statistics dashboard (total users, total passwords, average per user)
- Two tabs:
  - **View All Users**: Search, view, edit, and delete users
  - **Add New User**: Form to create new users
- Search functionality
- Edit user details
- Delete user with confirmation
- Data table display

---

##### `page_view_passwords() -> None`

Render the view all passwords page.

**Features:**
- View all saved passwords with user information
- Filter by user
- Data table display
- Download as CSV
- Delete individual passwords
- Empty state handling

---

## Main Application

### main.py

Location: `src/main.py`

Main entry point for the Streamlit application.

#### Functions

##### `main() -> None`

Main application function that:
1. Sets up page configuration
2. Applies custom CSS styling
3. Initializes the database
4. Renders sidebar navigation
5. Routes to the selected page
6. Renders footer

**Page Configuration:**
- Title: "🔐 Password Generator"
- Icon: "🔑"
- Layout: Wide
- Sidebar: Expanded by default

**Navigation Pages:**
- 🔑 Generate Password
- 👥 Manage Users
- 🔐 View All Passwords

---

### run.py

Location: `run.py`

Launcher script for the application.

#### Functions

##### `main()`

Launch the Streamlit application using subprocess.

**Features:**
- Locates src/main.py
- Launches Streamlit server
- Handles KeyboardInterrupt gracefully
- Provides error messages for common issues

**Usage:**
```bash
python run.py
```

---

## Testing

### test_generator.py

Location: `tests/test_generator.py`

Unit tests for password generation functions.

**Test Classes:**
- `TestGeneratePin`: Tests for PIN generation
- `TestGenerateText`: Tests for text-only passwords
- `TestGenerateMixed`: Tests for mixed passwords
- `TestGenerateStrong`: Tests for strong passwords
- `TestGeneratePassword`: Tests for the main generation function
- `TestRandomness`: Tests for randomness and uniqueness

**Run Tests:**
```bash
pytest tests/test_generator.py
```

---

### test_crud.py

Location: `tests/test_crud.py`

Unit tests for database CRUD operations.

**Test Classes:**
- `TestUserCRUD`: Tests for user operations
- `TestPasswordCRUD`: Tests for password operations
- `TestDataIntegrity`: Tests for edge cases and data integrity

**Features:**
- Uses temporary database for testing
- Tests all CRUD operations
- Tests cascade delete functionality
- Tests search functionality
- Tests data validation

**Run Tests:**
```bash
pytest tests/test_crud.py
```

---

## Usage Examples

### Example 1: Generate a Strong Password

```python
from src.core.generator import generate_password
from src.core.validators import get_password_strength

# Generate a strong password
password = generate_password("STRONG", 20)
print(f"Password: {password}")

# Check its strength
strength = get_password_strength(password)
print(f"Strength: {strength}")
```

### Example 2: Create User and Save Password

```python
from src.database import create_user, create_password
from src.core.generator import generate_password

# Create a user
user_id = create_user("John", "Doe")

# Generate and save a password
password = generate_password("MIXED", 16)
password_id = create_password(user_id, password, "MIXED", 16)

print(f"User ID: {user_id}")
print(f"Password ID: {password_id}")
```

### Example 3: Retrieve All Passwords

```python
from src.database import get_all_passwords
import pandas as pd

# Get all passwords
passwords = get_all_passwords()

# Convert to DataFrame for analysis
df = pd.DataFrame(passwords)
print(df[['full_name', 'mode', 'length', 'created_at']])
```

### Example 4: Search and Update Users

```python
from src.database import search_users, update_user

# Search for users
results = search_users("John")

# Update the first result
if results:
    user_id = results[0]['id']
    success = update_user(user_id, "Jonathan", "Doe")
    print(f"Update successful: {success}")
```

### Example 5: Validate Input

```python
from src.core.validators import validate_name, validate_password_length

# Validate a name
is_valid, error = validate_name("John")
if not is_valid:
    print(f"Error: {error}")

# Validate password length
is_valid, error = validate_password_length(16)
if is_valid:
    print("Length is valid!")
```

---

## Architecture Overview

### Module Dependencies

```
main.py
├── database/
│   ├── db.py
│   ├── models.py
│   └── crud.py
├── core/
│   ├── generator.py
│   └── validators.py
├── ui/
│   ├── pages.py
│   └── components.py
└── config/
    └── settings.py
```

### Data Flow

1. **User Input** → UI Components (pages.py)
2. **Validation** → validators.py
3. **Password Generation** → generator.py
4. **Database Operations** → crud.py → db.py
5. **Display** → components.py → Streamlit UI

---

## Security Considerations

⚠️ **Important Security Notes:**

1. **Password Storage**: Passwords are stored in **plain text** in the SQLite database. For production use:
   - Implement password hashing (bcrypt, Argon2)
   - Use encryption for the database file
   - Consider encrypted vault solutions

2. **Random Generation**: Uses Python's `random` module, which is **not cryptographically secure**. For production:
   - Use `secrets` module instead
   - Consider hardware random number generators

3. **Access Control**: No authentication is implemented. For production:
   - Add user authentication
   - Implement role-based access control
   - Use secure session management

4. **Input Validation**: While basic validation is implemented, consider:
   - SQL injection prevention (already handled via parameterized queries)
   - XSS prevention in the UI
   - Rate limiting for password generation

---

## Performance Considerations

- Database uses indexes on frequently queried columns
- Foreign key constraints enabled for data integrity
- Context managers ensure proper connection cleanup
- Batch operations available via get_all_* functions

---

## Future Enhancements

Potential areas for improvement:
- Password encryption in database
- Password history tracking
- Password expiration dates
- Export to other formats (JSON, Excel)
- Batch password generation
- Custom character sets
- Password templates
- Dark mode support
- Mobile responsive design improvements

---

**End of Documentation**

For questions or contributions, please refer to the main README.md file.
