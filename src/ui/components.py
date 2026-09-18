"""
Reusable UI components for the Streamlit application.

This module contains reusable components like headers, footers,
info boxes, and other UI elements.
"""

import streamlit as st
from typing import Optional


def render_page_header(title: str, icon: str = "🔐", subtitle: Optional[str] = None) -> None:
    """
    Render a consistent page header.

    Args:
        title: The page title
        icon: Icon emoji (default: "🔐")
        subtitle: Optional subtitle text
    """
    st.markdown(f"# {icon} {title}")
    if subtitle:
        st.markdown(f"*{subtitle}*")
    st.markdown("---")


def render_info_box(message: str, type: str = "info") -> None:
    """
    Render an info/warning/error box.

    Args:
        message: The message to display
        type: Type of box - "info", "success", "warning", "error"
    """
    if type == "info":
        st.info(message)
    elif type == "success":
        st.success(message)
    elif type == "warning":
        st.warning(message)
    elif type == "error":
        st.error(message)


def render_strength_indicator(strength: str) -> None:
    """
    Render a password strength indicator with color coding.

    Args:
        strength: Strength level ("Weak", "Medium", "Strong")
    """
    colors = {
        "Weak": "🔴",
        "Medium": "🟡",
        "Strong": "🟢"
    }

    color_styles = {
        "Weak": "#ff4b4b",
        "Medium": "#ffa500",
        "Strong": "#00cc00"
    }

    emoji = colors.get(strength, "⚪")
    color = color_styles.get(strength, "#888888")

    st.markdown(
        f"""
        <div style="padding: 10px; border-radius: 5px; background-color: {color}20; border-left: 4px solid {color};">
            <strong>{emoji} Password Strength: {strength}</strong>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_password_display(password: str, strength: str) -> None:
    """
    Render the generated password with a copy button and strength indicator.

    Args:
        password: The password to display
        strength: Password strength level
    """
    st.markdown("### Generated Password")

    # Display password in a code block
    st.code(password, language=None)

    # Display strength indicator
    render_strength_indicator(strength)

    # Copy to clipboard button using text_input
    st.text_input(
        "Click to select and copy:",
        value=password,
        key=f"copy_{password}",
        help="Select all (Ctrl+A) and copy (Ctrl+C)"
    )


def render_stats_card(label: str, value: int, icon: str = "📊") -> None:
    """
    Render a statistics card.

    Args:
        label: The stat label
        value: The stat value
        icon: Icon emoji
    """
    st.markdown(
        f"""
        <div style="padding: 20px; border-radius: 10px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; text-align: center; margin: 10px 0;">
            <div style="font-size: 2em;">{icon}</div>
            <div style="font-size: 2.5em; font-weight: bold; margin: 10px 0;">{value}</div>
            <div style="font-size: 1.1em;">{label}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_empty_state(message: str, icon: str = "📭") -> None:
    """
    Render an empty state message.

    Args:
        message: The message to display
        icon: Icon emoji
    """
    st.markdown(
        f"""
        <div style="text-align: center; padding: 60px 20px; color: #888;">
            <div style="font-size: 4em; margin-bottom: 20px;">{icon}</div>
            <div style="font-size: 1.3em;">{message}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_user_card(user: dict, show_actions: bool = True) -> None:
    """
    Render a user information card.

    Args:
        user: User dictionary with id, first_name, last_name, created_at
        show_actions: Whether to show action buttons
    """
    st.markdown(
        f"""
        <div style="padding: 15px; border-radius: 8px; background-color: #f0f2f6; margin: 10px 0; border-left: 4px solid #667eea;">
            <div style="font-size: 1.2em; font-weight: bold;">
                👤 {user['first_name']} {user['last_name']}
            </div>
            <div style="color: #666; font-size: 0.9em; margin-top: 5px;">
                ID: {user['id']} | Created: {user['created_at']}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_password_card(password_entry: dict) -> None:
    """
    Render a password entry card.

    Args:
        password_entry: Password dictionary with all fields
    """
    mode_icons = {
        "PIN": "🔢",
        "TEXT": "🔤",
        "MIXED": "🔀",
        "STRONG": "💪"
    }

    icon = mode_icons.get(password_entry['mode'], "🔑")

    st.markdown(
        f"""
        <div style="padding: 15px; border-radius: 8px; background-color: #f0f2f6; margin: 10px 0;">
            <div style="font-size: 1.1em; font-weight: bold;">
                {icon} {password_entry['mode']} Password (Length: {password_entry['length']})
            </div>
            <div style="font-family: monospace; font-size: 1.2em; margin: 10px 0; padding: 10px; background-color: white; border-radius: 4px;">
                {password_entry['password']}
            </div>
            <div style="color: #666; font-size: 0.85em;">
                User: {password_entry.get('full_name', 'Unknown')} | Created: {password_entry['created_at']}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_footer() -> None:
    """
    Render the application footer.
    """
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; color: #888; padding: 20px;">
            🔐 Password Generator v1.0.0 | Built with Streamlit & Python
        </div>
        """,
        unsafe_allow_html=True
    )
