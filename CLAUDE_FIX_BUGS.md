# CLAUDE.md - Fix Bullets, Session, and Errors

## 4 Issues to Fix

1. Bullets still inline in report
2. Session lost on page refresh (need persistent login)
3. KeyError: 'priority_matrix' not initialized
4. WeasyPrint PDF export failing (missing system library)

---

## Issue 1: Bullets STILL on Same Line

The LLM is ignoring line break instructions. Need to force it in post-processing.

**In modules/report_generator.py, add this function:**

```python
import re

def fix_bullet_formatting(text: str) -> str:
    """
    Force bullets onto separate lines.
    Handles: "• Item 1 • Item 2" -> "• Item 1\n• Item 2"
    """
    # Pattern: bullet followed by text, then another bullet
    # Replace the space-bullet with newline-bullet
    
    # First, normalize any weird bullet characters
    text = text.replace('●', '•').replace('○', '•').replace('-', '•')
    
    # Split on bullet and rejoin with newlines
    # This handles: "• A • B • C" -> "• A\n• B\n• C"
    parts = re.split(r'\s*•\s*', text)
    
    # Filter empty parts and rejoin
    parts = [p.strip() for p in parts if p.strip()]
    
    if len(parts) > 1:
        return '• ' + '\n• '.join(parts)
    elif len(parts) == 1:
        return '• ' + parts[0]
    return text


def fix_all_bullet_sections(report: str) -> str:
    """Fix bullet formatting in all sections of the report."""
    
    # Find sections that have bullets
    sections = [
        "Platform Features:",
        "MCP Tools:",
        "What's Coming:",
        "AI Agents:",
        "Available Today:",
    ]
    
    for section in sections:
        # Find content after section header until next section or double newline
        pattern = rf'(\*\*{re.escape(section)}\*\*\s*)(.*?)(?=\n\n|\*\*[A-Z]|\Z)'
        
        def fix_match(match):
            header = match.group(1)
            content = match.group(2)
            fixed_content = fix_bullet_formatting(content)
            return header + '\n' + fixed_content
        
        report = re.sub(pattern, fix_match, report, flags=re.DOTALL)
    
    return report
```

**Apply AFTER getting synthesis:**

```python
def generate_report(...):
    # ... generate report ...
    
    # Fix bullet formatting as final step
    report = fix_all_bullet_sections(report)
    
    return report
```

**ALSO update the synthesis prompt to be MORE explicit:**

```python
SYNTHESIS_SYSTEM_PROMPT = """
...

BULLET FORMATTING RULE (CRITICAL):
When listing items with bullets, EACH bullet MUST start on a NEW LINE.

WRONG FORMAT (never do this):
• Item 1 • Item 2 • Item 3

CORRECT FORMAT (always do this):
• Item 1
• Item 2
• Item 3

This rule is MANDATORY for all bullet lists.
...
"""
```

---

## Issue 2: Session Lost on Refresh - Add Persistent Login

**Create modules/session_manager.py:**

```python
import streamlit as st
import json
import hashlib
import os
from datetime import datetime, timedelta
from pathlib import Path

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


def load_session(token: str) -> dict | None:
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


def get_session_token_from_cookie() -> str | None:
    """Get session token from query params (acts like cookie)."""
    return st.query_params.get("session", None)


def set_session_cookie(token: str):
    """Set session token in query params."""
    st.query_params["session"] = token


def clear_session_cookie():
    """Clear session token from query params."""
    if "session" in st.query_params:
        del st.query_params["session"]
```

**Update modules/auth.py:**

```python
from modules.session_manager import (
    generate_session_token,
    save_session,
    load_session,
    delete_session,
    get_session_token_from_cookie,
    set_session_cookie,
    clear_session_cookie
)

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


def logout():
    """Log out user and clear session."""
    token = st.session_state.get("session_token")
    
    if token:
        delete_session(token)
        clear_session_cookie()
    
    # Clear session state
    st.session_state["authenticated"] = False
    st.session_state["user"] = None
    st.session_state["session_token"] = None
    
    st.rerun()
```

**Update login form to use login_user():**

```python
# In render_login_form(), after validation:
if submitted and is_authorized(email):
    user_data = {
        "name": name.strip(),
        "email": email.strip().lower(),
        "company": company.strip() if company else "Unknown",
        "login_time": datetime.now().isoformat()
    }
    login_user(user_data)  # Use new function
    st.rerun()
```

**Add logout button to sidebar:**

```python
# In app.py sidebar:
with st.sidebar:
    if st.session_state.get("authenticated"):
        user = st.session_state.get("user", {})
        st.markdown(f"**👤 {user.get('name', 'User')}**")
        st.caption(user.get('email', ''))
        
        if st.button("🚪 Logout", use_container_width=True):
            logout()
```

---

## Issue 3: KeyError 'priority_matrix'

Initialize all session state variables at the start of app.py:

```python
# At TOP of app.py, after imports:

def init_session_state():
    """Initialize all session state variables."""
    defaults = {
        "authenticated": False,
        "user": None,
        "session_token": None,
        "selected_capability": None,
        "generated_report": None,
        "priority_matrix": None,
        "report": None,
        "scores": {},
        "show_zero_warning": False,
        "confirm_generate": False,
    }
    
    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

# Call immediately after imports
init_session_state()
```

**Also fix the line that's failing:**

```python
# WRONG - assumes key exists:
pm = st.session_state['priority_matrix']

# CORRECT - use .get() with default:
pm = st.session_state.get('priority_matrix', None)

# OR check first:
if st.session_state.get('priority_matrix'):
    pm = st.session_state['priority_matrix']
    # use pm...
```

---

## Issue 4: WeasyPrint PDF Export Failing

WeasyPrint requires system libraries (libgobject, pango, cairo) not available on Railway.

**Solution: Switch to a different PDF library that doesn't need system deps.**

**Option A: Use markdown-pdf or pdfkit (needs wkhtmltopdf)**

**Option B: Use reportlab (pure Python)**

**Option C: Use fpdf2 (pure Python, recommended)**

**Update modules/export_handler.py:**

```python
from fpdf import FPDF
import markdown
import re

def export_to_pdf(report_markdown: str, company_name: str = "") -> bytes:
    """Export report to PDF using fpdf2 (pure Python, no system deps)."""
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Set font
    pdf.set_font("Helvetica", size=10)
    
    # Title
    pdf.set_font("Helvetica", "B", size=16)
    pdf.cell(0, 10, f"O2C Assessment Report", ln=True, align="C")
    if company_name:
        pdf.set_font("Helvetica", size=12)
        pdf.cell(0, 10, company_name, ln=True, align="C")
    pdf.ln(10)
    
    # Process markdown to text
    lines = report_markdown.split('\n')
    
    for line in lines:
        line = line.strip()
        
        if not line:
            pdf.ln(5)
            continue
        
        # Headers
        if line.startswith('### '):
            pdf.set_font("Helvetica", "B", size=12)
            pdf.multi_cell(0, 6, line.replace('### ', ''))
            pdf.set_font("Helvetica", size=10)
        elif line.startswith('## '):
            pdf.set_font("Helvetica", "B", size=14)
            pdf.multi_cell(0, 8, line.replace('## ', ''))
            pdf.set_font("Helvetica", size=10)
        elif line.startswith('# '):
            pdf.set_font("Helvetica", "B", size=16)
            pdf.multi_cell(0, 10, line.replace('# ', ''))
            pdf.set_font("Helvetica", size=10)
        
        # Bold text
        elif line.startswith('**') and line.endswith('**'):
            pdf.set_font("Helvetica", "B", size=10)
            pdf.multi_cell(0, 6, line.replace('**', ''))
            pdf.set_font("Helvetica", size=10)
        
        # Bullets
        elif line.startswith('• ') or line.startswith('- '):
            pdf.set_x(15)  # Indent
            pdf.multi_cell(0, 5, line)
        
        # Regular text
        else:
            # Remove markdown formatting
            clean_line = re.sub(r'\*\*(.*?)\*\*', r'\1', line)  # Bold
            clean_line = re.sub(r'\*(.*?)\*', r'\1', clean_line)  # Italic
            pdf.multi_cell(0, 5, clean_line)
    
    return pdf.output()


def export_to_docx(report_markdown: str, company_name: str = "") -> bytes:
    """Export to Word document."""
    from docx import Document
    from docx.shared import Pt, Inches
    from io import BytesIO
    
    doc = Document()
    
    # Title
    title = doc.add_heading("O2C Assessment Report", 0)
    if company_name:
        doc.add_paragraph(company_name)
    
    # Process markdown
    lines = report_markdown.split('\n')
    
    for line in lines:
        line = line.strip()
        
        if not line:
            continue
        
        if line.startswith('### '):
            doc.add_heading(line.replace('### ', ''), level=3)
        elif line.startswith('## '):
            doc.add_heading(line.replace('## ', ''), level=2)
        elif line.startswith('# '):
            doc.add_heading(line.replace('# ', ''), level=1)
        elif line.startswith('• ') or line.startswith('- '):
            doc.add_paragraph(line[2:], style='List Bullet')
        else:
            doc.add_paragraph(line)
    
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer.getvalue()
```

**Update requirements.txt:**

```
# Remove weasyprint
# Add:
fpdf2>=2.7.0
```

**Update the download button in app.py:**

```python
# PDF download
if st.session_state.get('report'):
    col1, col2 = st.columns(2)
    
    with col1:
        pdf_bytes = export_to_pdf(
            st.session_state['report'], 
            st.session_state.get('user', {}).get('company', '')
        )
        st.download_button(
            "📥 Download PDF",
            pdf_bytes,
            file_name="o2c_assessment.pdf",
            mime="application/pdf"
        )
    
    with col2:
        docx_bytes = export_to_docx(
            st.session_state['report'],
            st.session_state.get('user', {}).get('company', '')
        )
        st.download_button(
            "📥 Download Word",
            docx_bytes,
            file_name="o2c_assessment.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
```

---

## Summary

| Issue | Fix |
|-------|-----|
| Inline bullets | Post-process with `fix_all_bullet_sections()` regex |
| Session lost | Use query params as cookie + file-based sessions |
| KeyError | Initialize all session state at app start |
| WeasyPrint | Replace with fpdf2 (pure Python) |

## Requirements.txt Update

```
# Remove:
weasyprint

# Add:
fpdf2>=2.7.0
```
