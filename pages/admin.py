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
        col1, col2, col3 = st.columns([2, 4, 1])
        with col1:
            st.text(user.get('name', 'N/A'))
        with col2:
            st.text(user.get('email', 'N/A'))
        with col3:
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
name,email
John Smith,john@acme.com
Jane Doe,jane@acme.com
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
    col1, col2 = st.columns(2)
    with col1:
        new_name = st.text_input("Name")
    with col2:
        new_email = st.text_input("Email")

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
                    "name": new_name.strip() or new_email.split('@')[0]
                })
                save_allowed_users(users)
                st.success(f"✅ Added {new_email}")
                st.rerun()

st.markdown("---")

# Download current list
st.subheader("📥 Export Current Users")

if users:
    csv_content = "name,email\n"
    for user in users:
        csv_content += f"{user.get('name','')},{user.get('email','')}\n"

    st.download_button(
        "Download as CSV",
        csv_content,
        file_name="allowed_users.csv",
        mime="text/csv"
    )
