# modules/auth.py
import streamlit as st
import hashlib
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

from config import USER_LOGS_DIR
from modules.admin import load_allowed_users as load_users_from_file
from modules.session_manager import (
    generate_session_token,
    save_session,
    load_session,
    delete_session,
    get_session_token_from_cookie,
    set_session_cookie,
    clear_session_cookie
)

# Allowed users - fallback if no file uploaded
ALLOWED_USERS = [
    "john.smith@company.com",
    "jane.doe@company.com",
    "alex.johnson@company.com",
    # Add more emails as needed
]

# Load from uploaded users file or environment variable
def get_allowed_users() -> list:
    """Get allowed user emails from uploaded file, env, or fallback list."""
    # First try: uploaded users file
    users = load_users_from_file()
    if users:
        return [u['email'].lower() for u in users]

    # Second try: environment variable
    env_users = os.getenv("ALLOWED_USERS", "")
    if env_users:
        return [email.strip().lower() for email in env_users.split(",")]

    # Fallback: default list
    return [email.lower() for email in ALLOWED_USERS]


def get_user_info(email: str) -> dict:
    """Get full user info from allowed list."""
    users = load_users_from_file()
    for user in users:
        if user['email'].lower() == email.lower():
            return user
    return {"email": email, "name": email.split('@')[0]}


def is_authorized(email: str) -> bool:
    """Check if email is in allowed list."""
    return email.lower().strip() in get_allowed_users()


def render_login_form() -> Optional[dict]:
    """Render login form and return user info if valid."""

    st.markdown("""
    <div style="max-width: 400px; margin: 100px auto; padding: 40px;
                background: #1e1e1e; border-radius: 10px; border: 1px solid #333;">
        <h2 style="text-align: center; margin-bottom: 20px;">🔐 O2C Assessment</h2>
        <p style="text-align: center; color: #888; margin-bottom: 30px;">
            Please enter your details to continue
        </p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("login_form"):
        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:
            name = st.text_input("Name", placeholder="John Smith")
            email = st.text_input("Email", placeholder="john.smith@company.com")

            submitted = st.form_submit_button("Continue", use_container_width=True)

            if submitted:
                if not name or not email:
                    st.error("Please enter both name and email")
                    return None

                if not is_authorized(email):
                    st.error("⚠️ Email not authorized. Contact your administrator.")
                    return None

                # Store user session with persistent token
                user_data = {
                    "name": name.strip(),
                    "email": email.strip().lower(),
                    "login_time": datetime.now().isoformat(),
                    "session_id": hashlib.md5(f"{email}{datetime.now()}".encode()).hexdigest()[:12]
                }

                # Use login_user for persistent session
                login_user(user_data)

                st.rerun()

    return None


def check_authentication() -> bool:
    """Check if user is authenticated via session state or cookie."""

    # Already authenticated in this session
    if st.session_state.get("authenticated", False):
        return True

    # Check for session cookie/token
    token = get_session_token_from_cookie()
    if token:
        user_data = load_session(token)
        if user_data:
            # Restore session
            st.session_state["authenticated"] = True
            st.session_state["user"] = user_data
            st.session_state["session_token"] = token
            return True

    return False


def get_current_user() -> Optional[dict]:
    """Get current user data."""
    return st.session_state.get("user", None)


def login_user(user_data: dict):
    """Log in user and create persistent session."""
    token = generate_session_token(user_data["email"])

    # Save to file
    save_session(user_data, token)

    # Set in session state
    st.session_state["authenticated"] = True
    st.session_state["user"] = user_data
    st.session_state["session_token"] = token

    # Set cookie
    set_session_cookie(token)

    # Log login
    log_user_activity(user_data, "login")


def logout():
    """Log out user and clear session."""
    # Log logout first
    if "user" in st.session_state:
        log_user_activity(st.session_state["user"], "logout")

    token = st.session_state.get("session_token")

    if token:
        delete_session(token)
        clear_session_cookie()

    # Clear session state
    st.session_state["authenticated"] = False
    st.session_state["user"] = None
    st.session_state["session_token"] = None

    st.rerun()


def log_user_activity(user: dict, activity: str, data: dict = None):
    """Log user activity to Railway Volume."""
    log_dir = Path(USER_LOGS_DIR)
    log_dir.mkdir(exist_ok=True)

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "user_email": user["email"],
        "user_name": user["name"],
        "session_id": user["session_id"],
        "activity": activity,
        "data": data
    }

    # Append to daily log file
    log_file = log_dir / f"activity_{datetime.now().strftime('%Y-%m-%d')}.jsonl"
    with open(log_file, "a") as f:
        f.write(json.dumps(log_entry) + "\n")
