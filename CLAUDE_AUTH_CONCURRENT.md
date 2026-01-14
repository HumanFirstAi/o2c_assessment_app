# CLAUDE.md - Authentication & Concurrency

## Task

Add user authentication (allowlist-based) and concurrent report generation.

---

## 1. Create auth.py Module

```python
# modules/auth.py
import streamlit as st
import hashlib
import json
import os
from datetime import datetime
from pathlib import Path

# Allowed users - add emails here
ALLOWED_USERS = [
    "john.smith@company.com",
    "jane.doe@company.com",
    "alex.johnson@company.com",
    # Add more emails as needed
]

# Or load from environment variable (comma-separated)
def get_allowed_users() -> list:
    """Get allowed users from env or default list."""
    env_users = os.getenv("ALLOWED_USERS", "")
    if env_users:
        return [email.strip().lower() for email in env_users.split(",")]
    return [email.lower() for email in ALLOWED_USERS]


def is_authorized(email: str) -> bool:
    """Check if email is in allowed list."""
    return email.lower().strip() in get_allowed_users()


def render_login_form() -> dict | None:
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
            name = st.text_input("Full Name", placeholder="John Smith")
            email = st.text_input("Email", placeholder="john.smith@company.com")
            company = st.text_input("Company", placeholder="Acme Corp")
            
            submitted = st.form_submit_button("Continue", use_container_width=True)
            
            if submitted:
                if not name or not email:
                    st.error("Please enter both name and email")
                    return None
                
                if not is_authorized(email):
                    st.error("⚠️ Email not authorized. Contact your administrator.")
                    return None
                
                # Store user session
                user_data = {
                    "name": name.strip(),
                    "email": email.strip().lower(),
                    "company": company.strip() if company else "Unknown",
                    "login_time": datetime.now().isoformat(),
                    "session_id": hashlib.md5(f"{email}{datetime.now()}".encode()).hexdigest()[:12]
                }
                
                st.session_state["user"] = user_data
                st.session_state["authenticated"] = True
                
                # Log login
                log_user_activity(user_data, "login")
                
                st.rerun()
    
    return None


def check_authentication() -> bool:
    """Check if user is authenticated."""
    return st.session_state.get("authenticated", False)


def get_current_user() -> dict | None:
    """Get current user data."""
    return st.session_state.get("user", None)


def logout():
    """Clear user session."""
    if "user" in st.session_state:
        log_user_activity(st.session_state["user"], "logout")
    st.session_state["authenticated"] = False
    st.session_state["user"] = None
    st.rerun()


def log_user_activity(user: dict, activity: str, data: dict = None):
    """Log user activity to file."""
    log_dir = Path("user_logs")
    log_dir.mkdir(exist_ok=True)
    
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "user_email": user["email"],
        "user_name": user["name"],
        "company": user["company"],
        "session_id": user["session_id"],
        "activity": activity,
        "data": data
    }
    
    # Append to daily log file
    log_file = log_dir / f"activity_{datetime.now().strftime('%Y-%m-%d')}.jsonl"
    with open(log_file, "a") as f:
        f.write(json.dumps(log_entry) + "\n")
```

---

## 2. Create Storage Module

```python
# modules/storage.py
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional
import hashlib

# Storage directory
STORAGE_DIR = Path(os.getenv("STORAGE_DIR", "user_data"))


def get_user_storage_path(email: str) -> Path:
    """Get storage directory for a user."""
    safe_email = hashlib.md5(email.encode()).hexdigest()[:16]
    user_dir = STORAGE_DIR / safe_email
    user_dir.mkdir(parents=True, exist_ok=True)
    return user_dir


def save_assessment(user: dict, scores: dict, report: str) -> str:
    """Save user's assessment and report."""
    user_dir = get_user_storage_path(user["email"])
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    assessment_id = f"{timestamp}_{user['session_id']}"
    
    # Save scores
    scores_file = user_dir / f"scores_{assessment_id}.json"
    scores_data = {
        "assessment_id": assessment_id,
        "user": user,
        "timestamp": datetime.now().isoformat(),
        "scores": scores
    }
    with open(scores_file, "w") as f:
        json.dump(scores_data, f, indent=2)
    
    # Save report
    report_file = user_dir / f"report_{assessment_id}.md"
    with open(report_file, "w") as f:
        f.write(report)
    
    return assessment_id


def get_user_assessments(email: str) -> list:
    """Get all assessments for a user."""
    user_dir = get_user_storage_path(email)
    
    assessments = []
    for scores_file in user_dir.glob("scores_*.json"):
        with open(scores_file) as f:
            data = json.load(f)
            assessments.append({
                "id": data["assessment_id"],
                "timestamp": data["timestamp"],
                "scores_file": str(scores_file),
                "report_file": str(scores_file).replace("scores_", "report_").replace(".json", ".md")
            })
    
    # Sort by timestamp descending
    assessments.sort(key=lambda x: x["timestamp"], reverse=True)
    return assessments


def load_assessment(email: str, assessment_id: str) -> Optional[dict]:
    """Load a specific assessment."""
    user_dir = get_user_storage_path(email)
    
    scores_file = user_dir / f"scores_{assessment_id}.json"
    report_file = user_dir / f"report_{assessment_id}.md"
    
    if not scores_file.exists():
        return None
    
    with open(scores_file) as f:
        data = json.load(f)
    
    if report_file.exists():
        with open(report_file) as f:
            data["report"] = f.read()
    
    return data
```

---

## 3. Create Concurrent Report Generator

```python
# modules/concurrent_generator.py
import asyncio
import concurrent.futures
from typing import Callable
import streamlit as st


def generate_report_concurrent(
    generate_func: Callable,
    scores: dict,
    knowledge_base: dict,
    company_name: str,
    max_workers: int = 3
) -> str:
    """
    Generate report with concurrent section processing.
    
    Splits synthesis into parallel tasks for:
    - Executive summary
    - Each urgent gap (parallel)
    - MCP sections (static, no wait)
    """
    
    from modules.report_generator import (
        analyze_all_scores,
        filter_by_importance_threshold,
        synthesize_with_claude,
        format_gap_context,
        format_executive_context,
        get_capability_from_kb,
        VALID_AGENTS,
        MCP_GUIDE_SECTION,
        AGENT_GUIDE_SECTION,
        generate_priority_matrix_table
    )
    
    # Step 1: Compute priorities (fast, no LLM)
    analyzed = analyze_all_scores(scores, knowledge_base)
    analyzed = filter_by_importance_threshold(analyzed)
    urgent_gaps = [c for c in analyzed if c['category'] == 'URGENT_GAP']
    
    # Calculate metrics
    all_i = [s['importance'] for s in analyzed]
    all_r = [s['readiness'] for s in analyzed]
    avg_importance = sum(all_i) / len(all_i) if all_i else 0
    avg_readiness = sum(all_r) / len(all_r) if all_r else 0
    
    # Step 2: Prepare all synthesis tasks
    tasks = []
    
    # Executive summary task
    exec_context = format_executive_context(
        company_name, len(analyzed), urgent_gaps, [],
        avg_importance, avg_readiness
    )
    tasks.append(("executive_summary", exec_context))
    
    # Gap tasks (one per gap)
    for gap in urgent_gaps:
        kb_data = get_capability_from_kb(gap['id'], knowledge_base)
        if kb_data:
            context = format_gap_context(gap, kb_data)
            tasks.append((f"gap_{gap['id']}", context, gap))
    
    # Step 3: Run synthesis concurrently
    results = {}
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_task = {}
        
        for task in tasks:
            if task[0] == "executive_summary":
                future = executor.submit(
                    synthesize_with_claude,
                    "executive_summary",
                    task[1],
                    VALID_AGENTS
                )
                future_to_task[future] = ("executive_summary", None)
            else:
                future = executor.submit(
                    synthesize_with_claude,
                    "urgent_gap",
                    task[1],
                    VALID_AGENTS
                )
                future_to_task[future] = ("gap", task[2])
        
        # Collect results as they complete
        for future in concurrent.futures.as_completed(future_to_task):
            task_type, gap_data = future_to_task[future]
            try:
                result = future.result()
                if task_type == "executive_summary":
                    results["executive_summary"] = result
                else:
                    results[gap_data['id']] = {
                        "gap": gap_data,
                        "synthesis": result
                    }
            except Exception as e:
                print(f"Synthesis error: {e}")
    
    # Step 4: Assemble report
    urgent_sections = []
    for gap in urgent_gaps:
        if gap['id'] in results:
            gap_result = results[gap['id']]
            section = f"### {gap['name']}\n**Phase:** {gap['phase']} | **Scores:** I={gap['importance']}, R={gap['readiness']}, Gap={gap.get('gap_score', 0)}\n\n{gap_result['synthesis']}"
            urgent_sections.append(section)
    
    report = f"""# O2C AI & MCP Readiness Assessment
## {company_name}
*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*

---

## 1. Executive Summary

{results.get('executive_summary', 'Unable to generate summary.')}

---

## 2. Priority Matrix

{generate_priority_matrix_table(analyzed)}

---

## 3. Urgent Gaps - Detailed Analysis

{chr(10).join(urgent_sections) if urgent_sections else "*No urgent gaps identified.*"}

---

## 4. Getting Started with Zuora MCP

{MCP_GUIDE_SECTION}

---

## 5. Building Your First Zuora Agent

{AGENT_GUIDE_SECTION}
"""
    
    return report
```

---

## 4. Update app.py

```python
# app.py - Updated with auth and storage
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

# Must be first Streamlit command
st.set_page_config(
    page_title="O2C Assessment",
    page_icon="📊",
    layout="wide"
)

from modules.auth import (
    check_authentication, 
    render_login_form, 
    get_current_user,
    logout,
    log_user_activity
)
from modules.storage import save_assessment, get_user_assessments
from modules.interactive_form import render_interactive_assessment
from modules.report_generator import generate_report
from modules.concurrent_generator import generate_report_concurrent

# Check API key
if not os.getenv("ANTHROPIC_API_KEY"):
    st.error("⚠️ ANTHROPIC_API_KEY not configured")
    st.stop()

# Authentication gate
if not check_authentication():
    render_login_form()
    st.stop()

# User is authenticated
user = get_current_user()

# Sidebar with user info
with st.sidebar:
    st.markdown(f"**👤 {user['name']}**")
    st.caption(f"{user['email']}")
    st.caption(f"🏢 {user['company']}")
    
    if st.button("Logout", use_container_width=True):
        logout()
    
    st.divider()
    
    # Previous assessments
    st.subheader("📁 Your Assessments")
    assessments = get_user_assessments(user['email'])
    
    if assessments:
        for assessment in assessments[:5]:  # Show last 5
            timestamp = assessment['timestamp'][:10]
            if st.button(f"📄 {timestamp}", key=assessment['id']):
                # Load previous assessment
                st.session_state['load_assessment'] = assessment['id']
                st.rerun()
    else:
        st.caption("No previous assessments")
    
    st.divider()
    
    # Progress
    st.subheader("Progress")
    # ... existing progress code ...

# Main content
st.title("O2C AI & MCP Readiness Assessment")
st.markdown(f"Welcome, **{user['name']}**")

# Render interactive assessment
render_interactive_assessment()

# Generate Report button
if st.button("📊 Generate Report", type="primary", use_container_width=True):
    with st.spinner("Generating report... This may take a minute."):
        # Collect scores from session state
        scores = collect_scores_from_session()
        
        # Log activity
        log_user_activity(user, "generate_report", {"score_count": len(scores)})
        
        # Generate with concurrency
        report = generate_report_concurrent(
            generate_func=generate_report,
            scores=scores,
            knowledge_base=knowledge_base,
            company_name=user['company'],
            max_workers=3
        )
        
        # Save to storage
        assessment_id = save_assessment(user, scores, report)
        
        # Log completion
        log_user_activity(user, "report_complete", {"assessment_id": assessment_id})
        
        # Display report
        st.session_state['generated_report'] = report
        st.session_state['assessment_id'] = assessment_id

# Display report if generated
if st.session_state.get('generated_report'):
    st.markdown("---")
    display_report_sections(st.session_state['generated_report'])
```

---

## 5. Environment Variables

Add to Railway:

```bash
# Allowed users (comma-separated)
ALLOWED_USERS=john@company.com,jane@company.com,alex@company.com

# Or in .env file
ALLOWED_USERS="john@company.com,jane@company.com,alex@company.com"
```

---

## 6. Create user_logs Directory

```bash
mkdir -p user_logs
mkdir -p user_data
```

Add to .gitignore:

```
user_logs/
user_data/
```

---

## 7. Update railway.json for Persistent Storage

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true",
    "healthcheckPath": "/",
    "healthcheckTimeout": 300
  }
}
```

Note: Railway ephemeral storage resets on redeploy. For persistent storage, 
connect a Railway Volume or external database (PostgreSQL, Redis, S3).

---

## File Checklist

```
modules/
├── auth.py                 (new)
├── storage.py              (new)
├── concurrent_generator.py (new)
├── interactive_form.py
├── report_generator.py
├── score_analyzer.py
└── export_handler.py

user_logs/                  (new - gitignored)
user_data/                  (new - gitignored)
```

---

## Concurrency Summary

| Section | Method |
|---------|--------|
| Executive Summary | Parallel thread |
| Gap 1 synthesis | Parallel thread |
| Gap 2 synthesis | Parallel thread |
| Gap 3 synthesis | Parallel thread |
| MCP Guide | Static (instant) |
| Agent Guide | Static (instant) |

With `max_workers=3`, multiple gaps synthesize simultaneously, 
reducing total report generation time by ~60%.
