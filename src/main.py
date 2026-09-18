"""
Main entry point for the Password Generator Streamlit application.

This is the main Streamlit application file that sets up the UI,
handles navigation, and initializes the database.
"""

import streamlit as st
import sys
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from database import init_database
from ui.pages import page_generate_password, page_manage_users, page_view_passwords
from ui.components import render_footer
from config import APP_TITLE, APP_ICON, VERSION


def main() -> None:
    """
    Main application function.

    Sets up the Streamlit page configuration, initializes the database,
    and handles page navigation.
    """
    # Page configuration
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon=APP_ICON,
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Custom CSS for better styling
    st.markdown(
        """
        <style>
        .main {
            padding-top: 2rem;
        }
        .stButton>button {
            width: 100%;
        }
        h1 {
            color: #667eea;
        }
        .stAlert {
            margin-top: 1rem;
            margin-bottom: 1rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Initialize database
    try:
        init_database()
    except Exception as e:
        st.error(f"❌ Failed to initialize database: {str(e)}")
        st.stop()

    # Sidebar navigation
    with st.sidebar:
        st.title(f"{APP_ICON} {APP_TITLE}")
        st.markdown(f"**Version:** {VERSION}")
        st.markdown("---")

        # Navigation menu
        st.subheader("📍 Navigation")

        page = st.radio(
            "Go to:",
            options=[
                "🔑 Generate Password",
                "👥 Manage Users",
                "🔐 View All Passwords"
            ],
            label_visibility="collapsed"
        )

        st.markdown("---")

        # Info section
        st.subheader("ℹ️ About")
        st.info(
            """
            **Password Generator** helps you create secure passwords
            and manage them with a local database.

            **Features:**
            - 4 password modes (PIN, TEXT, MIXED, STRONG)
            - User management (CRUD)
            - Password storage
            - Export to CSV
            """
        )

        st.markdown("---")
        st.markdown(
            """
            <div style="text-align: center; color: #888; font-size: 0.8em;">
                Built with ❤️ using Python & Streamlit
            </div>
            """,
            unsafe_allow_html=True
        )

    # Page routing
    if page == "🔑 Generate Password":
        page_generate_password()
    elif page == "👥 Manage Users":
        page_manage_users()
    elif page == "🔐 View All Passwords":
        page_view_passwords()

    # Footer
    render_footer()


if __name__ == "__main__":
    main()
