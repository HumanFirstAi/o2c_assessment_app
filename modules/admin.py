import os
import csv
import json
from pathlib import Path

# Storage path - uses Railway Volume or local
STORAGE_BASE = os.getenv("STORAGE_PATH", "local_data")
USERS_FILE = Path(STORAGE_BASE) / "allowed_users.json"


def load_allowed_users() -> list:
    """Load allowed users from storage."""
    if USERS_FILE.exists():
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return []


def save_allowed_users(users: list):
    """Save allowed users to storage."""
    USERS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)


def import_users_from_csv(csv_content: str) -> tuple[int, list]:
    """
    Import users from CSV content.
    Returns (count, errors)
    """
    users = []
    errors = []

    lines = csv_content.strip().split('\n')
    reader = csv.DictReader(lines)

    for i, row in enumerate(reader, start=2):
        email = row.get('email', '').strip().lower()
        name = row.get('name', '').strip()

        if not email:
            errors.append(f"Row {i}: Missing email")
            continue

        if '@' not in email:
            errors.append(f"Row {i}: Invalid email '{email}'")
            continue

        users.append({
            "email": email,
            "name": name or email.split('@')[0]
        })

    if users:
        save_allowed_users(users)

    return len(users), errors


def is_users_file_exists() -> bool:
    """Check if users file has been uploaded."""
    return USERS_FILE.exists() and len(load_allowed_users()) > 0


def get_admin_secret() -> str:
    """Get admin secret from environment."""
    return os.getenv("ADMIN_SECRET", "")


def delete_user(email: str) -> bool:
    """Remove a user from allowed list."""
    users = load_allowed_users()
    updated = [u for u in users if u['email'].lower() != email.lower()]
    if len(updated) < len(users):
        save_allowed_users(updated)
        return True
    return False
