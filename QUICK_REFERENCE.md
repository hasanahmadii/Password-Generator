# Password Generator - Quick Reference Guide

A cheat sheet for developers working with the Password Generator application.

---

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python run.py

# Or directly with Streamlit
streamlit run src/main.py

# Run tests
pytest tests/
```

---

## Common Operations

### Generate Passwords

```python
from src.core.generator import generate_password

# PIN (digits only)
pin = generate_password("PIN", 6)

# TEXT (letters only)
text = generate_password("TEXT", 12)

# MIXED (letters + digits)
mixed = generate_password("MIXED", 16)

# STRONG (letters + digits + symbols)
strong = generate_password("STRONG", 20)
```

### User Management

```python
from src.database.crud import create_user, get_user, update_user, delete_user

# Create
user_id = create_user("John", "Doe")

# Read
user = get_user(user_id)
all_users = get_all_users()

# Update
update_user(user_id, "Jane", "Doe")

# Delete
delete_user(user_id)
```

### Password Storage

```python
from src.database.crud import create_password, get_passwords_by_user

# Save password
password_id = create_password(
    user_id=1,
    password="MyP@ssw0rd",
    mode="STRONG",
    length=20
)

# Get user's passwords
passwords = get_passwords_by_user(user_id=1)
```

### Validation

```python
from src.core.validators import validate_name, validate_password_length, get_password_strength

# Validate name
is_valid, error = validate_name("John", "First Name")

# Validate length
is_valid, error = validate_password_length(16)

# Check strength
strength = get_password_strength("MyP@ssw0rd123")  # Returns: "Strong", "Medium", or "Weak"
```

---

## Project Structure

```
password_generator/
├── src/
│   ├── main.py              # Streamlit app entry
│   ├── core/                # Business logic
│   │   ├── generator.py     # Password generation
│   │   └── validators.py    # Input validation
│   ├── database/            # Data layer
│   │   ├── db.py           # Connection management
│   │   ├── models.py       # Schema definitions
│   │   └── crud.py         # Database operations
│   ├── ui/                  # User interface
│   │   ├── pages.py        # Main pages
│   │   └── components.py   # Reusable components
│   └── config/
│       └── settings.py     # Configuration
├── tests/                   # Test suite
├── data/                    # Database storage
├── run.py                   # Launcher script
└── requirements.txt
```

---

## Password Modes

| Mode   | Characters              | Use Case                    | Default Length |
|--------|-------------------------|-----------------------------|----------------|
| PIN    | 0-9                     | Numeric passwords, PINs     | 6              |
| TEXT   | a-z, A-Z                | Memorable passwords         | 12             |
| MIXED  | a-z, A-Z, 0-9           | Balanced security           | 16             |
| STRONG | a-z, A-Z, 0-9, symbols  | Maximum security            | 20             |

---

## Database Schema

### users
```sql
id (PK) | first_name | last_name | created_at
```

### passwords
```sql
id (PK) | user_id (FK) | password | mode | length | created_at
```

**Relationship**: One user → Many passwords (1:N)  
**Cascade**: Deleting a user deletes their passwords

---

## Configuration Constants

```python
# From src/config/settings.py

MIN_PASSWORD_LENGTH = 4
MAX_PASSWORD_LENGTH = 64
DEFAULT_PIN_LENGTH = 6
DEFAULT_TEXT_LENGTH = 12
DEFAULT_MIXED_LENGTH = 16
DEFAULT_STRONG_LENGTH = 20

APP_TITLE = "🔐 Password Generator"
VERSION = "1.0.0"
```

---

## UI Components

```python
from src.ui.components import (
    render_page_header,
    render_password_display,
    render_strength_indicator,
    render_stats_card,
    render_empty_state,
)

# Render page header
render_page_header("My Page", "🔑", "Subtitle here")

# Display password with strength
render_password_display(password, strength)

# Show strength indicator
render_strength_indicator("Strong")  # "Weak", "Medium", or "Strong"

# Stats card
render_stats_card("Total Users", 42, "👥")

# Empty state
render_empty_state("No data yet", "📭")
```

---

## Testing

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_generator.py

# Run with coverage
pytest --cov=src tests/

# Run with verbose output
pytest -v tests/

# Run specific test
pytest tests/test_generator.py::TestGeneratePin::test_default_length
```

---

## Common Patterns

### Database Context Manager

```python
from src.database.db import get_db_connection

with get_db_connection() as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    # Connection automatically closed
```

### Error Handling

```python
try:
    user_id = create_user("John", "Doe")
except Exception as e:
    print(f"Error: {e}")
```

### Search Users

```python
from src.database.crud import search_users

# Search by name
results = search_users("John")
for user in results:
    print(f"{user['first_name']} {user['last_name']}")
```

### Export to CSV

```python
import pandas as pd
from src.database.crud import get_all_passwords

passwords = get_all_passwords()
df = pd.DataFrame(passwords)
df.to_csv("passwords_export.csv", index=False)
```

---

## Troubleshooting

### Database Issues

```python
# Check if database exists
from src.database.db import check_database_exists
exists = check_database_exists()

# Re-initialize database
from src.database.db import init_database
init_database()
```

### Import Issues

Make sure you're in the project root or add to path:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
```

### Streamlit Port Already in Use

```bash
# Use different port
streamlit run src/main.py --server.port 8502
```

---

## Development Tips

1. **Virtual Environment**: Always use a virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

2. **Database Location**: `data/app.db` (auto-created on first run)

3. **Hot Reload**: Streamlit auto-reloads when files change

4. **Session State**: Use `st.session_state` for preserving data across reruns

5. **Testing**: Write tests before making changes to ensure nothing breaks

---

## API Shortcuts

### Most Used Functions

```python
# Generation
from src.core.generator import generate_password
password = generate_password("STRONG", 20)

# User CRUD
from src.database.crud import create_user, get_all_users, delete_user
user_id = create_user("John", "Doe")
users = get_all_users()
delete_user(user_id)

# Password CRUD
from src.database.crud import create_password, get_all_passwords
pwd_id = create_password(user_id, password, "STRONG", 20)
all_passwords = get_all_passwords()

# Validation
from src.core.validators import validate_name, get_password_strength
is_valid, error = validate_name("John")
strength = get_password_strength(password)
```

---

## Security Notes

⚠️ **Educational Project - Not Production Ready**

- Passwords stored in plain text
- Uses `random` module (not cryptographically secure)
- No authentication/authorization
- No encryption

**For Production**: Use `secrets` module, hash passwords, encrypt database, add authentication

---

## Version Information

- **Current Version**: 1.0.0
- **Python**: 3.11+
- **Streamlit**: 1.32+
- **Database**: SQLite3

---

## Links

- [Full Documentation](DOCUMENTATION.md)
- [README](README.md)
- [Tests](tests/)

---

**Last Updated**: September 18, 2026
