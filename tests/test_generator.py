"""
Unit tests for password generator functions.

Tests all password generation modes: PIN, TEXT, MIXED, and STRONG.
"""

import pytest
import string
from src.core.generator import (
    generate_pin,
    generate_text,
    generate_mixed,
    generate_strong,
    generate_password
)


class TestGeneratePin:
    """Test PIN generation (digits only)."""

    def test_default_length(self):
        """Test PIN generation with default length."""
        pin = generate_pin()
        assert len(pin) == 6
        assert pin.isdigit()

    def test_custom_length(self):
        """Test PIN generation with custom length."""
        for length in [4, 6, 8, 10]:
            pin = generate_pin(length)
            assert len(pin) == length
            assert pin.isdigit()

    def test_only_digits(self):
        """Test that PIN contains only digits."""
        pin = generate_pin(20)
        assert all(c in string.digits for c in pin)


class TestGenerateText:
    """Test TEXT generation (letters only)."""

    def test_default_length(self):
        """Test text generation with default length."""
        text = generate_text()
        assert len(text) == 12
        assert text.isalpha()

    def test_custom_length(self):
        """Test text generation with custom length."""
        for length in [8, 12, 16, 20]:
            text = generate_text(length)
            assert len(text) == length
            assert text.isalpha()

    def test_only_letters(self):
        """Test that text contains only letters."""
        text = generate_text(30)
        assert all(c in string.ascii_letters for c in text)


class TestGenerateMixed:
    """Test MIXED generation (letters + digits)."""

    def test_default_length(self):
        """Test mixed generation with default length."""
        mixed = generate_mixed()
        assert len(mixed) == 16
        assert mixed.isalnum()

    def test_custom_length(self):
        """Test mixed generation with custom length."""
        for length in [10, 16, 20, 24]:
            mixed = generate_mixed(length)
            assert len(mixed) == length
            assert mixed.isalnum()

    def test_only_letters_and_digits(self):
        """Test that mixed contains only letters and digits."""
        mixed = generate_mixed(40)
        allowed = string.ascii_letters + string.digits
        assert all(c in allowed for c in mixed)


class TestGenerateStrong:
    """Test STRONG generation (letters + digits + symbols)."""

    def test_default_length(self):
        """Test strong generation with default length."""
        strong = generate_strong()
        assert len(strong) == 20

    def test_custom_length(self):
        """Test strong generation with custom length."""
        for length in [12, 16, 20, 24]:
            strong = generate_strong(length)
            assert len(strong) == length

    def test_contains_all_categories(self):
        """Test that strong password contains all character types."""
        # Generate multiple passwords to ensure consistency
        for _ in range(10):
            strong = generate_strong(20)

            has_lower = any(c in string.ascii_lowercase for c in strong)
            has_upper = any(c in string.ascii_uppercase for c in strong)
            has_digit = any(c in string.digits for c in strong)
            has_symbol = any(c in string.punctuation for c in strong)

            # For length >= 4, all categories should be present
            assert has_lower
            assert has_upper
            assert has_digit
            assert has_symbol

    def test_short_length(self):
        """Test strong generation with very short length."""
        strong = generate_strong(4)
        assert len(strong) == 4


class TestGeneratePassword:
    """Test the main generate_password function."""

    def test_pin_mode(self):
        """Test password generation in PIN mode."""
        password = generate_password("PIN", 8)
        assert len(password) == 8
        assert password.isdigit()

    def test_text_mode(self):
        """Test password generation in TEXT mode."""
        password = generate_password("TEXT", 12)
        assert len(password) == 12
        assert password.isalpha()

    def test_mixed_mode(self):
        """Test password generation in MIXED mode."""
        password = generate_password("MIXED", 16)
        assert len(password) == 16
        assert password.isalnum()

    def test_strong_mode(self):
        """Test password generation in STRONG mode."""
        password = generate_password("STRONG", 20)
        assert len(password) == 20

    def test_invalid_mode(self):
        """Test that invalid mode raises ValueError."""
        with pytest.raises(ValueError) as excinfo:
            generate_password("INVALID", 10)
        assert "Invalid password mode" in str(excinfo.value)

    def test_all_modes_different_lengths(self):
        """Test all modes with various lengths."""
        modes = ["PIN", "TEXT", "MIXED", "STRONG"]
        lengths = [6, 10, 15, 20]

        for mode in modes:
            for length in lengths:
                password = generate_password(mode, length)
                assert len(password) == length


class TestRandomness:
    """Test randomness and uniqueness of generated passwords."""

    def test_generates_different_passwords(self):
        """Test that multiple generations produce different results."""
        passwords = [generate_password("STRONG", 16) for _ in range(100)]

        # All passwords should be unique
        assert len(passwords) == len(set(passwords))

    def test_pin_randomness(self):
        """Test that PINs are sufficiently random."""
        pins = [generate_pin(6) for _ in range(100)]

        # Should have good variety (at least 90 unique out of 100)
        assert len(set(pins)) >= 90
