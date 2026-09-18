"""
Streamlit UI pages for the Password Generator application.

This module contains the three main pages:
1. Generate Password
2. Manage Users
3. View All Passwords
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from typing import Optional

from core.generator import generate_password
from core.validators import validate_name, validate_password_length, get_password_strength
from database.crud import (
    create_user,
    get_all_users,
    update_user,
    delete_user,
    create_password,
    get_all_passwords,
    delete_password,
    get_user_count,
    get_password_count,
    search_users,
)
from config import (
    MIN_PASSWORD_LENGTH,
    MAX_PASSWORD_LENGTH,
    DEFAULT_PIN_LENGTH,
    DEFAULT_TEXT_LENGTH,
    DEFAULT_MIXED_LENGTH,
    DEFAULT_STRONG_LENGTH,
)
from ui.components import (
    render_page_header,
    render_password_display,
    render_stats_card,
    render_empty_state,
    render_info_box,
)


def page_generate_password() -> None:
    """
    Render the password generation page.

    This page allows users to:
    - Enter their name
    - Select password mode and length
    - Generate passwords
    - Save passwords to database
    """
    render_page_header(
        "Generate Password",
        "🔑",
        "Create secure passwords in multiple modes"
    )

    # Initialize session state for generated password
    if 'generated_password' not in st.session_state:
        st.session_state.generated_password = None
        st.session_state.password_mode = None
        st.session_state.password_length = None
        st.session_state.password_strength = None

    # User Information Section
    st.subheader("👤 User Information")

    col1, col2 = st.columns(2)

    with col1:
        first_name = st.text_input(
            "First Name *",
            placeholder="Enter your first name",
            help="Required field"
        )

    with col2:
        last_name = st.text_input(
            "Last Name *",
            placeholder="Enter your last name",
            help="Required field"
        )

    # Password Configuration Section
    st.subheader("🔧 Password Configuration")

    col1, col2 = st.columns(2)

    with col1:
        mode = st.selectbox(
            "Password Mode",
            options=["PIN", "TEXT", "MIXED", "STRONG"],
            help="PIN: digits only | TEXT: letters only | MIXED: letters+digits | STRONG: letters+digits+symbols"
        )

    with col2:
        # Set default length based on mode
        default_lengths = {
            "PIN": DEFAULT_PIN_LENGTH,
            "TEXT": DEFAULT_TEXT_LENGTH,
            "MIXED": DEFAULT_MIXED_LENGTH,
            "STRONG": DEFAULT_STRONG_LENGTH,
        }

        length = st.slider(
            "Password Length",
            min_value=MIN_PASSWORD_LENGTH,
            max_value=MAX_PASSWORD_LENGTH,
            value=default_lengths[mode],
            help=f"Choose a length between {MIN_PASSWORD_LENGTH} and {MAX_PASSWORD_LENGTH}"
        )

    # Generate Button
    st.markdown("###")
    if st.button("🎲 Generate Password", type="primary", use_container_width=True):
        # Validate inputs
        is_valid_first, error_first = validate_name(first_name, "First Name")
        is_valid_last, error_last = validate_name(last_name, "Last Name")
        is_valid_length, error_length = validate_password_length(length)

        errors = []
        if not is_valid_first:
            errors.append(error_first)
        if not is_valid_last:
            errors.append(error_last)
        if not is_valid_length:
            errors.append(error_length)

        if errors:
            for error in errors:
                st.error(error)
        else:
            try:
                # Generate password
                password = generate_password(mode, length)
                strength = get_password_strength(password)

                # Store in session state
                st.session_state.generated_password = password
                st.session_state.password_mode = mode
                st.session_state.password_length = length
                st.session_state.password_strength = strength
                st.session_state.user_first_name = first_name.strip()
                st.session_state.user_last_name = last_name.strip()

                st.success("✅ Password generated successfully!")

            except Exception as e:
                st.error(f"❌ Error generating password: {str(e)}")

    # Display generated password
    if st.session_state.generated_password:
        st.markdown("---")
        render_password_display(
            st.session_state.generated_password,
            st.session_state.password_strength
        )

        # Save to Database Button
        st.markdown("###")
        col1, col2 = st.columns([3, 1])

        with col1:
            save_to_db = st.checkbox("💾 Save this password to database", value=True)

        with col2:
            if st.button("💾 Save", type="primary", disabled=not save_to_db):
                try:
                    # Create or find user
                    user_id = create_user(
                        st.session_state.user_first_name,
                        st.session_state.user_last_name
                    )

                    # Save password
                    password_id = create_password(
                        user_id,
                        st.session_state.generated_password,
                        st.session_state.password_mode,
                        st.session_state.password_length
                    )

                    st.success(f"✅ Password saved successfully! (ID: {password_id})")

                except Exception as e:
                    st.error(f"❌ Error saving password: {str(e)}")


def page_manage_users() -> None:
    """
    Render the user management page.

    This page allows users to:
    - View all users
    - Add new users
    - Edit existing users
    - Delete users
    """
    render_page_header(
        "Manage Users",
        "👥",
        "Create, update, and delete user accounts"
    )

    # Stats Section
    try:
        user_count = get_user_count()
        col1, col2, col3 = st.columns(3)

        with col1:
            render_stats_card("Total Users", user_count, "👥")

        with col2:
            password_count = get_password_count()
            render_stats_card("Total Passwords", password_count, "🔐")

        with col3:
            avg = password_count / user_count if user_count > 0 else 0
            render_stats_card("Avg per User", round(avg, 1), "📊")

    except Exception as e:
        st.error(f"Error loading stats: {str(e)}")

    st.markdown("---")

    # Two tabs: View Users and Add User
    tab1, tab2 = st.tabs(["📋 View All Users", "➕ Add New User"])

    with tab1:
        # Search functionality
        search_term = st.text_input("🔍 Search users", placeholder="Search by first name or last name")

        try:
            if search_term:
                users = search_users(search_term)
            else:
                users = get_all_users()

            if not users:
                render_empty_state("No users found", "👤")
            else:
                st.markdown(f"### Found {len(users)} user(s)")

                # Convert to DataFrame for better display
                df = pd.DataFrame(users)
                df = df[['id', 'first_name', 'last_name', 'created_at']]
                df.columns = ['ID', 'First Name', 'Last Name', 'Created At']

                st.dataframe(df, use_container_width=True, hide_index=True)

                # Edit/Delete Section
                st.markdown("---")
                st.subheader("✏️ Edit or Delete User")

                user_ids = [u['id'] for u in users]
                user_options = [f"{u['id']} - {u['first_name']} {u['last_name']}" for u in users]

                selected_option = st.selectbox("Select a user", user_options)
                selected_user_id = int(selected_option.split(" - ")[0])

                # Get selected user details
                selected_user = next(u for u in users if u['id'] == selected_user_id)

                col1, col2 = st.columns(2)

                with col1:
                    edit_first_name = st.text_input(
                        "First Name",
                        value=selected_user['first_name'],
                        key="edit_first"
                    )

                with col2:
                    edit_last_name = st.text_input(
                        "Last Name",
                        value=selected_user['last_name'],
                        key="edit_last"
                    )

                col1, col2 = st.columns(2)

                with col1:
                    if st.button("💾 Update User", type="primary", use_container_width=True):
                        is_valid_first, error_first = validate_name(edit_first_name, "First Name")
                        is_valid_last, error_last = validate_name(edit_last_name, "Last Name")

                        if not is_valid_first:
                            st.error(error_first)
                        elif not is_valid_last:
                            st.error(error_last)
                        else:
                            try:
                                success = update_user(selected_user_id, edit_first_name, edit_last_name)
                                if success:
                                    st.success("✅ User updated successfully!")
                                    st.rerun()
                                else:
                                    st.error("❌ User not found")
                            except Exception as e:
                                st.error(f"❌ Error updating user: {str(e)}")

                with col2:
                    if st.button("🗑️ Delete User", type="secondary", use_container_width=True):
                        # Confirmation
                        if 'confirm_delete' not in st.session_state:
                            st.session_state.confirm_delete = False

                        if not st.session_state.confirm_delete:
                            st.session_state.confirm_delete = True
                            st.warning("⚠️ Click Delete again to confirm. This will delete all passwords for this user!")
                        else:
                            try:
                                success = delete_user(selected_user_id)
                                if success:
                                    st.success("✅ User deleted successfully!")
                                    st.session_state.confirm_delete = False
                                    st.rerun()
                                else:
                                    st.error("❌ User not found")
                            except Exception as e:
                                st.error(f"❌ Error deleting user: {str(e)}")

        except Exception as e:
            st.error(f"❌ Error loading users: {str(e)}")

    with tab2:
        st.subheader("➕ Add New User")

        with st.form("add_user_form"):
            col1, col2 = st.columns(2)

            with col1:
                new_first_name = st.text_input("First Name *", placeholder="Enter first name")

            with col2:
                new_last_name = st.text_input("Last Name *", placeholder="Enter last name")

            submitted = st.form_submit_button("➕ Add User", type="primary", use_container_width=True)

            if submitted:
                is_valid_first, error_first = validate_name(new_first_name, "First Name")
                is_valid_last, error_last = validate_name(new_last_name, "Last Name")

                if not is_valid_first:
                    st.error(error_first)
                elif not is_valid_last:
                    st.error(error_last)
                else:
                    try:
                        user_id = create_user(new_first_name, new_last_name)
                        st.success(f"✅ User created successfully! (ID: {user_id})")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error creating user: {str(e)}")


def page_view_passwords() -> None:
    """
    Render the view all passwords page.

    This page allows users to:
    - View all saved passwords
    - Filter by user
    - Delete passwords
    - Download as CSV
    """
    render_page_header(
        "View All Passwords",
        "🔐",
        "Browse and manage all saved passwords"
    )

    try:
        passwords = get_all_passwords()

        if not passwords:
            render_empty_state("No passwords saved yet", "🔐")
            return

        st.markdown(f"### Total: {len(passwords)} password(s)")

        # Filter by user
        users = get_all_users()
        user_options = ["All Users"] + [f"{u['id']} - {u['first_name']} {u['last_name']}" for u in users]
        selected_filter = st.selectbox("🔍 Filter by user", user_options)

        # Apply filter
        if selected_filter != "All Users":
            filter_user_id = int(selected_filter.split(" - ")[0])
            passwords = [p for p in passwords if p['user_id'] == filter_user_id]

        # Convert to DataFrame
        df = pd.DataFrame(passwords)
        display_df = df[['id', 'full_name', 'password', 'mode', 'length', 'created_at']].copy()
        display_df.columns = ['ID', 'User', 'Password', 'Mode', 'Length', 'Created At']

        st.dataframe(display_df, use_container_width=True, hide_index=True)

        # Download CSV
        csv = display_df.to_csv(index=False)
        st.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name=f"passwords_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )

        # Delete password section
        st.markdown("---")
        st.subheader("🗑️ Delete Password")

        password_options = [f"{p['id']} - {p['full_name']} - {p['mode']} ({p['password'][:10]}...)" for p in passwords]
        selected_password = st.selectbox("Select password to delete", password_options)
        selected_password_id = int(selected_password.split(" - ")[0])

        if st.button("🗑️ Delete Password", type="secondary"):
            try:
                success = delete_password(selected_password_id)
                if success:
                    st.success("✅ Password deleted successfully!")
                    st.rerun()
                else:
                    st.error("❌ Password not found")
            except Exception as e:
                st.error(f"❌ Error deleting password: {str(e)}")

    except Exception as e:
        st.error(f"❌ Error loading passwords: {str(e)}")
