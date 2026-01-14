# CLAUDE.md - Admin User Upload System

## Task

Create a one-time user upload system via CSV file for authentication.

---

## Files to Create

### 1. modules/admin.py

```python
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
        company = row.get('company', '').strip()
        
        if not email:
            errors.append(f"Row {i}: Missing email")
            continue
        
        if '@' not in email:
            errors.append(f"Row {i}: Invalid email '{email}'")
            continue
        
        users.append({
            "email": email,
            "name": name or email.split('@')[0],
            "company": company or "Unknown"
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
```

---

### 2. pages/admin.py

Create `pages` directory if it doesn't exist.

```python
import streamlit as st
import os
from modules.admin import (
    import_users_from_csv,
    load_allowed_users,
    save_allowed_users,
    is_users_file_exists,
    get_admin_secret,
    delete_user
)

st.set_page_config(page_title="Admin - User Management", page_icon="🔐")

st.title("🔐 Admin: User Management")

# Check admin secret
admin_secret = get_admin_secret()
if admin_secret:
    if "admin_authenticated" not in st.session_state:
        st.session_state.admin_authenticated = False
    
    if not st.session_state.admin_authenticated:
        entered_secret = st.text_input("Admin Secret", type="password")
        if st.button("Login"):
            if entered_secret == admin_secret:
                st.session_state.admin_authenticated = True
                st.rerun()
            else:
                st.error("Invalid secret")
        st.stop()

st.markdown("---")

# Show current users
st.subheader("📋 Current Allowed Users")
users = load_allowed_users()

if users:
    st.success(f"✅ {len(users)} users configured")
    
    # Display as table with delete buttons
    for i, user in enumerate(users):
        col1, col2, col3, col4 = st.columns([2, 3, 2, 1])
        with col1:
            st.text(user.get('name', 'N/A'))
        with col2:
            st.text(user.get('email', 'N/A'))
        with col3:
            st.text(user.get('company', 'N/A'))
        with col4:
            if st.button("🗑️", key=f"del_{i}", help=f"Remove {user['email']}"):
                delete_user(user['email'])
                st.rerun()
else:
    st.warning("⚠️ No users configured yet. Upload a CSV below.")

st.markdown("---")

# Upload section
st.subheader("📤 Upload User List (CSV)")

st.markdown("""
**CSV Format:**
```
name,email,company
John Smith,john@acme.com,Acme Corp
Jane Doe,jane@acme.com,Acme Corp
```
""")

uploaded_file = st.file_uploader("Choose CSV file", type=['csv'])

if uploaded_file:
    content = uploaded_file.read().decode('utf-8')
    
    st.markdown("**Preview:**")
    st.code(content[:500] + "..." if len(content) > 500 else content)
    
    col1, col2 = st.columns(2)
    with col1:
        replace = st.checkbox("Replace existing users", value=True)
    
    if st.button("✅ Import Users", type="primary"):
        if not replace:
            # Append to existing
            existing = load_allowed_users()
            count, errors = import_users_from_csv(content)
            if count > 0:
                combined = existing + load_allowed_users()
                # Dedupe by email
                seen = set()
                unique = []
                for u in combined:
                    if u['email'] not in seen:
                        seen.add(u['email'])
                        unique.append(u)
                save_allowed_users(unique)
                count = len(unique) - len(existing)
        else:
            count, errors = import_users_from_csv(content)
        
        if errors:
            for error in errors:
                st.error(error)
        
        if count > 0:
            st.success(f"✅ Imported {count} users!")
            st.rerun()
        else:
            st.error("No valid users found in CSV")

st.markdown("---")

# Manual add section
st.subheader("➕ Add Single User")

with st.form("add_user_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        new_name = st.text_input("Name")
    with col2:
        new_email = st.text_input("Email")
    with col3:
        new_company = st.text_input("Company")
    
    submitted = st.form_submit_button("Add User")
    
    if submitted:
        if not new_email or '@' not in new_email:
            st.error("Valid email required")
        else:
            users = load_allowed_users()
            # Check if already exists
            if any(u['email'].lower() == new_email.lower() for u in users):
                st.warning(f"{new_email} already exists")
            else:
                users.append({
                    "email": new_email.lower().strip(),
                    "name": new_name.strip() or new_email.split('@')[0],
                    "company": new_company.strip() or "Unknown"
                })
                save_allowed_users(users)
                st.success(f"✅ Added {new_email}")
                st.rerun()

st.markdown("---")

# Download current list
st.subheader("📥 Export Current Users")

if users:
    csv_content = "name,email,company\n"
    for user in users:
        csv_content += f"{user.get('name','')},{user.get('email','')},{user.get('company','')}\n"
    
    st.download_button(
        "Download as CSV",
        csv_content,
        file_name="allowed_users.csv",
        mime="text/csv"
    )
```

---

### 3. Update modules/auth.py

Replace the `get_allowed_users` function:

```python
# At top of modules/auth.py, add import:
from modules.admin import load_allowed_users

# Replace get_allowed_users function:
def get_allowed_users() -> list:
    """Get allowed user emails from uploaded file."""
    users = load_allowed_users()
    return [u['email'].lower() for u in users]


# Add helper function:
def get_user_info(email: str) -> dict:
    """Get full user info from allowed list."""
    users = load_allowed_users()
    for user in users:
        if user['email'].lower() == email.lower():
            return user
    return {"email": email, "name": email.split('@')[0], "company": "Unknown"}
```

---

### 4. Update app.py

Add this check after imports, before auth check:

```python
from modules.admin import is_users_file_exists

# Check if users have been configured (before auth check)
if not is_users_file_exists():
    st.warning("⚠️ No users configured yet.")
    st.info("An admin needs to upload the user list first.")
    st.markdown("[→ Go to Admin Page](/admin)")
    st.stop()
```

---

## Environment Variables

Add to Railway:

```
ADMIN_SECRET=your-secret-phrase-here
STORAGE_PATH=/data
```

---

## File Structure After Implementation

```
project/
├── app.py                    (updated)
├── pages/
│   └── admin.py              (new)
├── modules/
│   ├── admin.py              (new)
│   ├── auth.py               (updated)
│   ├── storage.py
│   ├── report_generator.py
│   └── ...
└── local_data/               (local dev)
    └── allowed_users.json    (created by upload)
```

---

## Usage Flow

### Admin Setup (one-time):

1. Go to `https://your-app.railway.app/admin`
2. Enter `ADMIN_SECRET`
3. Upload CSV with users:
   ```csv
   name,email,company
   John Smith,john@acme.com,Acme Corp
   Jane Doe,jane@acme.com,Acme Corp
   ```
4. Click "Import Users"

### User Login:

1. Go to main app
2. Enter name and email
3. If email is in allowed list → access granted
4. If not → "Email not authorized"

---

## Sample CSV Template

Create `sample_users.csv`:

```csv
name,email,company
John Smith,john.smith@acme.com,Acme Corp
Jane Doe,jane.doe@acme.com,Acme Corp
Alex Johnson,alex@partner.com,Partner Inc
Bob Wilson,bob@client.com,Client LLC
Sarah Brown,sarah@agency.com,Agency Co
```
