import streamlit as st
import json
import hashlib
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

# Import file locking (fcntl for Unix, msvcrt for Windows)
if sys.platform == "win32":
    import msvcrt
    USE_FCNTL = False
else:
    import fcntl
    USE_FCNTL = True

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
    """
    Save session to file with file locking to prevent race conditions.
    Uses atomic write (temp file + rename) for safety.
    """
    session_file = SESSION_DIR / f"{token}.json"
    temp_file = SESSION_DIR / f".{token}.json.tmp"

    session_data = {
        "user": user_data,
        "created_at": datetime.now().isoformat(),
        "expires_at": (datetime.now() + timedelta(days=SESSION_DURATION_DAYS)).isoformat()
    }

    try:
        # Write to temp file with exclusive lock
        with open(temp_file, "w") as f:
            if USE_FCNTL:
                fcntl.flock(f, fcntl.LOCK_EX)  # Exclusive lock
            json.dump(session_data, f)
            # Lock released when file closes

        # Atomic rename
        temp_file.rename(session_file)
    except Exception as e:
        # Cleanup temp file on error
        if temp_file.exists():
            temp_file.unlink()
        raise e


def load_session(token: str) -> Optional[dict]:
    """
    Load and validate session from file with shared lock.
    Prevents TOCTOU race conditions.
    """
    session_file = SESSION_DIR / f"{token}.json"

    if not session_file.exists():
        return None

    try:
        with open(session_file, "r") as f:
            # Acquire shared read lock
            if USE_FCNTL:
                fcntl.flock(f, fcntl.LOCK_SH)  # Shared lock for reading
            session_data = json.load(f)
            # Lock released when file closes

        # Check expiration
        expires_at = datetime.fromisoformat(session_data["expires_at"])
        if datetime.now() > expires_at:
            # Delete expired session with exclusive lock
            delete_session(token)
            return None

        return session_data["user"]
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return None


def delete_session(token: str):
    """
    Delete session file with exclusive lock.
    Prevents race condition if multiple processes try to delete same session.
    """
    session_file = SESSION_DIR / f"{token}.json"

    if not session_file.exists():
        return

    try:
        # Open with exclusive access for deletion
        with open(session_file, "r") as f:
            if USE_FCNTL:
                fcntl.flock(f, fcntl.LOCK_EX)  # Exclusive lock
            # Lock held during deletion

        # Delete file (lock released when file closed above)
        session_file.unlink(missing_ok=True)
    except FileNotFoundError:
        # Already deleted by another process - safe to ignore
        pass


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
