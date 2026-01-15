import streamlit as st
import json
import hashlib
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

# Session storage path
SESSION_DIR = Path(os.getenv("STORAGE_PATH", "local_data")) / "sessions"
SESSION_DIR.mkdir(parents=True, exist_ok=True)

# Session duration
SESSION_DURATION_DAYS = 7


def generate_session_token(email: str) -> str:
    """Generate a unique session token."""
    data = f"{email}{datetime.now().isoformat()}{os.urandom(16).hex()}"
    return hashlib.sha256(data.encode()).hexdigest()[:32]


def save_session(user_data: dict, token: str):
    """Save session to file."""
    session_file = SESSION_DIR / f"{token}.json"
    session_data = {
        "user": user_data,
        "created_at": datetime.now().isoformat(),
        "expires_at": (datetime.now() + timedelta(days=SESSION_DURATION_DAYS)).isoformat()
    }
    with open(session_file, "w") as f:
        json.dump(session_data, f)


def load_session(token: str) -> Optional[dict]:
    """Load and validate session from file."""
    session_file = SESSION_DIR / f"{token}.json"

    if not session_file.exists():
        return None

    try:
        with open(session_file) as f:
            session_data = json.load(f)

        # Check expiration
        expires_at = datetime.fromisoformat(session_data["expires_at"])
        if datetime.now() > expires_at:
            session_file.unlink()  # Delete expired session
            return None

        return session_data["user"]
    except:
        return None


def delete_session(token: str):
    """Delete session file."""
    session_file = SESSION_DIR / f"{token}.json"
    if session_file.exists():
        session_file.unlink()


def get_session_token_from_cookie() -> Optional[str]:
    """Get session token from query params (acts like cookie)."""
    return st.query_params.get("session", None)


def set_session_cookie(token: str):
    """Set session token in query params."""
    st.query_params["session"] = token


def clear_session_cookie():
    """Clear session token from query params."""
    if "session" in st.query_params:
        del st.query_params["session"]
