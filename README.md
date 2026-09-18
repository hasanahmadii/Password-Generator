# 🔐 Password Generator

A powerful desktop application built with Python and Streamlit for generating secure passwords with multiple modes and managing them in a local SQLite database.

![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)
![Streamlit](https://img.shields.io/badge/streamlit-1.32%2B-red)
![License](https://img.shields.io/badge/license-MIT-green)

## 📋 Table of Contents

- [Features](#features)
- [Screenshots](#screenshots)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Password Modes](#password-modes)
- [Database Schema](#database-schema)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

- **4 Password Generation Modes**
  - 🔢 PIN: Digits only (0-9)
  - 🔤 TEXT: Letters only (a-z, A-Z)
  - 🔀 MIXED: Letters + Digits
  - 💪 STRONG: Letters + Digits + Symbols

- **User Management**
  - Create, Read, Update, Delete (CRUD) operations
  - Search functionality
  - User statistics

- **Password Management**
  - Save generated passwords to database
  - View all saved passwords
  - Filter passwords by user
  - Delete individual passwords
  - Export to CSV

- **Password Strength Indicator**
  - Real-time strength evaluation
  - Color-coded indicators (Weak/Medium/Strong)

- **Modern UI**
  - Clean and intuitive interface
  - Responsive design
  - Interactive components
  - Statistics dashboard

## 📸 Screenshots

> Screenshots will be added here

### Generate Password Page
![Generate Password](screenshots/generate.png)

### Manage Users Page
![Manage Users](screenshots/users.png)

### View Passwords Page
![View Passwords](screenshots/passwords.png)

## 🚀 Installation

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/password_generator.git
cd password_generator
```

### Step 2: Create a Virtual Environment (Recommended)

```bash
# On Linux/Mac
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## 💻 Usage

### Method 1: Using the Launcher Script

```bash
python run.py
```

### Method 2: Direct Streamlit Command

```bash
streamlit run src/main.py
```

The application will open in your default web browser at `http://localhost:8501`

## 📁 Project Structure

```
password_generator/
│
├── src/
│   ├── __init__.py
│   ├── main.py                 # Streamlit entry point
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── pages.py            # UI pages/sections
│   │   └── components.py       # Reusable UI components
│   ├── core/
│   │   ├── __init__.py
│   │   ├── generator.py        # Password generation logic
│   │   └── validators.py       # Input validation
│   ├── database/
│   │   ├── __init__.py
│   │   ├── db.py               # Database connection
│   │   ├── models.py           # Table definitions
│   │   └── crud.py             # CRUD operations
│   └── config/
│       ├── __init__.py
│       └── settings.py         # Configuration constants
│
├── data/
│   └── app.db                  # SQLite database (auto-created)
│
├── tests/
│   ├── __init__.py
│   ├── test_generator.py
│   └── test_crud.py
│
├── .gitignore
├── README.md
├── requirements.txt
└── run.py                      # Application launcher
```

## 🛠️ Tech Stack

- **Language**: Python 3.11+
- **GUI Framework**: Streamlit
- **Database**: SQLite3
- **Data Processing**: Pandas
- **Password Generation**: random + string modules

## 🔑 Password Modes

### PIN Mode 🔢
- Contains only digits (0-9)
- Ideal for numeric passwords and PINs
- Recommended length: 4-8 characters

### TEXT Mode 🔤
- Contains only letters (a-z, A-Z)
- Good for memorable passwords
- Recommended length: 12-16 characters

### MIXED Mode 🔀
- Contains letters and digits
- Balanced security and usability
- Recommended length: 16-20 characters

### STRONG Mode 💪
- Contains letters, digits, and symbols
- Maximum security
- Guaranteed to have at least one character from each category
- Recommended length: 20+ characters

## 🗄️ Database Schema

### users Table
| Column      | Type      | Description                    |
|-------------|-----------|--------------------------------|
| id          | INTEGER   | Primary key (auto-increment)   |
| first_name  | TEXT      | User's first name              |
| last_name   | TEXT      | User's last name               |
| created_at  | TIMESTAMP | Record creation timestamp      |

### passwords Table
| Column      | Type      | Description                    |
|-------------|-----------|--------------------------------|
| id          | INTEGER   | Primary key (auto-increment)   |
| user_id     | INTEGER   | Foreign key to users(id)       |
| password    | TEXT      | Generated password             |
| mode        | TEXT      | Password mode (PIN/TEXT/etc)   |
| length      | INTEGER   | Password length                |
| created_at  | TIMESTAMP | Record creation timestamp      |

**Relationships**: 
- One user can have multiple passwords (1:N)
- CASCADE delete: When a user is deleted, all their passwords are deleted

## 🧪 Testing

Run the test suite:

```bash
# Install pytest if not already installed
pip install pytest

# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_generator.py

# Run with coverage
pytest --cov=src tests/
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see below for details:

```
MIT License

Copyright (c) 2026 Password Generator

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 👨‍💻 Author

Created with ❤️ by the Password Generator Team

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Icons from emoji standards
- Inspired by modern password management tools

---

**Note**: This application stores passwords in a local SQLite database. For production use with sensitive data, consider implementing additional security measures such as encryption.
