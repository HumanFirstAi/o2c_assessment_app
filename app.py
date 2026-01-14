import streamlit as st
import json
import random
import os
from dotenv import load_dotenv

load_dotenv()

from modules.auth import (
    check_authentication,
    render_login_form,
    get_current_user,
    logout,
    log_user_activity
)
from modules.storage import save_assessment, get_user_assessments, load_assessment
from modules.interactive_form import (
    render_interactive_assessment,
    save_assessment_json,
    collect_scores_for_analysis
)
from modules.score_analyzer import analyze_capabilities, create_priority_matrix
from modules.report_generator import generate_strategic_report
from modules.concurrent_generator import generate_report_concurrent
from modules.export_handler import export_to_docx, export_to_pdf, export_to_markdown
from grid_layout import GRID_LAYOUT

# Page config - responsive settings
st.set_page_config(
    page_title="O2C AI Readiness Assessment",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="auto"  # Collapses on mobile
)

# Inject viewport meta tag for mobile responsiveness
st.components.v1.html("""
<script>
if (!document.querySelector('meta[name="viewport"]')) {
    const meta = document.createElement('meta');
    meta.name = 'viewport';
    meta.content = 'width=device-width, initial-scale=1.0, maximum-scale=5.0';
    document.head.appendChild(meta);
}
</script>
""", height=0)

# Verify API key on startup
if not os.getenv("ANTHROPIC_API_KEY"):
    st.error("⚠️ ANTHROPIC_API_KEY not configured. Set it in Railway dashboard or environment.")
    st.stop()

# Verify storage on startup
import config
if os.path.exists(config.USER_DATA_DIR):
    print(f"✅ Storage mounted: {config.USER_DATA_DIR}")
else:
    print(f"⚠️ Storage not found: {config.USER_DATA_DIR}")

# Check if users have been configured
from modules.admin import is_users_file_exists

if not is_users_file_exists():
    st.warning("⚠️ No users configured yet.")
    st.info("An admin needs to upload the user list first.")
    st.markdown("### [→ Go to Admin Page](/admin)")
    st.markdown("Upload a CSV file with user emails to enable access.")
    st.stop()

# Authentication gate
if not check_authentication():
    render_login_form()
    st.stop()

# User is authenticated
user = get_current_user()


def init_test_mode():
    """Check for test mode and populate random scores."""
    query_params = st.query_params
    test_type = query_params.get("test")

    if test_type and "test_initialized" not in st.session_state:
        st.session_state.test_initialized = True
        st.session_state.interactive_scores = {}

        # Populate random scores for all 42 capabilities
        for row_idx, row in enumerate(GRID_LAYOUT):
            for col_idx, cell in enumerate(row):
                if cell is not None:  # Skip empty cells
                    cap_id = cell['id']
                    phase_id = cell['phase_id']

                    if test_type == "urgent":
                        # High importance, low readiness (urgent gaps)
                        importance = random.randint(7, 10)
                        readiness = random.randint(1, 4)

                    elif test_type == "strong":
                        # High importance, high readiness (strengths)
                        importance = random.randint(7, 10)
                        readiness = random.randint(7, 10)

                    elif test_type == "mixed":
                        # Realistic distribution
                        importance = random.choices([3,4,5,6,7,8,9], weights=[5,10,15,20,25,15,10])[0]
                        readiness = random.choices([2,3,4,5,6,7,8], weights=[10,15,20,25,15,10,5])[0]

                    else:  # test=true or any other value
                        # Pure random
                        importance = random.randint(1, 10)
                        readiness = random.randint(1, 10)

                    st.session_state.interactive_scores[cap_id] = {
                        "importance": importance,
                        "readiness": readiness,
                        "phase_id": phase_id
                    }

        st.toast(f"🧪 Test mode activated: {test_type.upper()} scenario loaded!", icon="✅")


# Initialize test mode if URL parameter present
init_test_mode()

# Load knowledge base
@st.cache_data
def load_knowledge_base():
    with open("knowledge_base.json") as f:
        return json.load(f)

kb = load_knowledge_base()

# Add responsive CSS for the entire app (hidden from display)
st.markdown("""
<div style="display: none;">
<style type="text/css">
/* Global responsive styles */
@media (max-width: 768px) {
    /* Mobile: Make main content full width */
    .main .block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        padding-top: 1rem !important;
        max-width: 100% !important;
    }

    /* Mobile: Larger headings for readability */
    h1 {
        font-size: 1.75rem !important;
        line-height: 1.2 !important;
    }
    h2 {
        font-size: 1.5rem !important;
        line-height: 1.3 !important;
    }
    h3 {
        font-size: 1.25rem !important;
        line-height: 1.4 !important;
    }

    /* Mobile: Increase paragraph text size */
    p {
        font-size: 16px !important;
        line-height: 1.6 !important;
    }

    /* Mobile: Full width buttons with touch-friendly size */
    .stButton button {
        width: 100%;
        min-height: 48px;
        font-size: 16px;
        padding: 12px 24px;
    }

    /* Mobile: Stack metric columns */
    [data-testid="metric-container"] {
        min-width: 100% !important;
        margin-bottom: 0.5rem;
    }

    /* Mobile: Better spacing between elements */
    .element-container {
        margin-bottom: 1rem;
    }

    /* Mobile: Full width text inputs */
    .stTextInput input {
        font-size: 16px;
        min-height: 44px;
        padding: 10px;
    }

    /* Mobile: Progress bar improvements */
    .stProgress {
        margin: 1rem 0;
    }

    /* Mobile: Download buttons */
    .stDownloadButton button {
        width: 100%;
        min-height: 48px;
        font-size: 16px;
        margin-bottom: 0.5rem;
    }

    /* Mobile: Expander improvements */
    .streamlit-expanderHeader {
        font-size: 16px;
        padding: 12px;
    }

    /* Mobile: Alert/warning boxes */
    .stAlert {
        padding: 1rem;
        font-size: 14px;
    }

    /* Mobile: Better markdown rendering */
    .markdown-text-container {
        font-size: 16px;
        line-height: 1.6;
    }

    /* Mobile: Stack columns vertically */
    [data-testid="column"] {
        min-width: 100% !important;
        flex: 1 1 100% !important;
        margin-bottom: 1rem;
    }

    /* Mobile: Spinner text */
    .stSpinner > div {
        font-size: 16px;
    }
}

@media (min-width: 769px) and (max-width: 1024px) {
    /* Tablet: Moderate adjustments */
    .main .block-container {
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }

    h1 {
        font-size: 2rem !important;
    }
    h2 {
        font-size: 1.75rem !important;
    }

    /* Tablet: Slightly larger touch targets */
    .stButton button,
    .stDownloadButton button {
        min-height: 44px;
        font-size: 15px;
    }
}

@media (min-width: 1025px) {
    /* Desktop: Default Streamlit behavior with minor enhancements */
    .main .block-container {
        max-width: 1200px;
    }
}

/* Print styles */
@media print {
    .stButton, .stDownloadButton, [data-testid="stSidebar"] {
        display: none !important;
    }
}
</style>
</div>
""", unsafe_allow_html=True)

# Header
st.title("🎯 O2C AI Agent & MCP Readiness Assessment")

# Test mode indicator
if st.query_params.get("test"):
    test_type = st.query_params.get("test")
    st.warning(f"🧪 **TEST MODE ACTIVE**: {test_type.upper()} scenario with randomly generated scores (42 capabilities populated)")

st.markdown("""
Transform your O2C assessment into an intelligent, AI-powered strategic roadmap.
Complete the interactive grid below to score each capability.
""")

# Sidebar with user info
with st.sidebar:
    # User info section
    st.markdown(f"**👤 {user['name']}**")
    st.caption(f"{user['email']}")

    if st.button("Logout", use_container_width=True):
        logout()

    st.divider()

    # Previous assessments
    st.subheader("📁 Your Assessments")
    assessments = get_user_assessments(user['email'])

    if assessments:
        for assessment in assessments[:5]:  # Show last 5
            timestamp = assessment['timestamp'][:10]
            if st.button(f"📄 {timestamp}", key=assessment['id'], use_container_width=True):
                # Load previous assessment
                loaded = load_assessment(user['email'], assessment['id'])
                if loaded:
                    st.session_state['interactive_scores'] = loaded['scores']
                    if 'report' in loaded:
                        st.session_state['report'] = loaded['report']
                    st.toast(f"✅ Loaded assessment from {timestamp}", icon="📄")
                    st.rerun()
    else:
        st.caption("No previous assessments")

    st.divider()

    # Progress tracking
    st.subheader("Progress")
    if 'interactive_scores' in st.session_state and st.session_state.interactive_scores:
        scores = st.session_state.interactive_scores
        # Only count capabilities where BOTH I and R are > 0
        completed = sum(1 for cap_id, data in scores.items()
                       if data.get("importance", 0) > 0 and data.get("readiness", 0) > 0)
        total = 42
        st.progress(min(completed / total, 1.0))
        st.caption(f"{completed}/{total} capabilities scored")
    else:
        st.caption("Start scoring capabilities below")

    st.divider()

    # Export JSON
    st.subheader("Export")
    if 'interactive_scores' in st.session_state and st.session_state.interactive_scores:
        customer_context = {"user": user['name'], "email": user['email']}
        json_data = save_assessment_json(
            st.session_state.interactive_scores,
            customer_context
        )

        if st.download_button(
            label="💾 Download JSON",
            data=json_data,
            file_name=f"O2C_Assessment_{user['name'].replace(' ', '_')}.json",
            mime="application/json",
            use_container_width=True
        ):
            st.toast("✅ JSON downloaded!", icon="💾")

# ============================================================================
# INTERACTIVE ASSESSMENT
# ============================================================================
st.markdown("---")
st.header("📝 Interactive Assessment")
st.markdown("""
Each capability card allows you to enter **I** (Importance) and **R** (Readiness) scores from 1-10.
""")

# Render the interactive grid
interactive_scores = render_interactive_assessment(kb)

# Helper functions for zero handling
def count_zero_capabilities(scores: dict) -> int:
    """Count capabilities with 0 in either I or R."""
    count = 0
    for cap_id, data in scores.items():
        if data.get("importance", 0) == 0 or data.get("readiness", 0) == 0:
            count += 1
    return count


def filter_valid_scores(scores: dict) -> dict:
    """Filter out capabilities where either I or R is 0."""
    return {
        cap_id: data
        for cap_id, data in scores.items()
        if data.get("importance", 0) > 0 and data.get("readiness", 0) > 0
    }


# Generate Report button with concurrent synthesis and storage
st.markdown("---")
if st.button("🚀 Generate Strategic Report", type="primary", use_container_width=True):
    if not interactive_scores:
        st.error("Please fill in at least some capability scores before generating a report.")
    else:
        # Check for zero values
        zero_count = count_zero_capabilities(interactive_scores)

        if zero_count > 0:
            st.session_state['show_zero_warning'] = True
            st.session_state['zero_count'] = zero_count
        else:
            st.session_state['confirm_generate'] = True

# Show warning dialog if there are zeros
if st.session_state.get('show_zero_warning', False):
    st.warning(f"⚠️ You have left some values as 0. **{st.session_state['zero_count']} capabilities** with 0 in either Importance or Readiness will be ignored and not assessed.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("❌ Cancel", use_container_width=True):
            st.session_state['show_zero_warning'] = False
            st.rerun()
    with col2:
        if st.button("✅ Continue", type="primary", use_container_width=True):
            st.session_state['show_zero_warning'] = False
            st.session_state['confirm_generate'] = True
            st.rerun()

# Actually generate report
if st.session_state.get('confirm_generate', False):
    st.session_state['confirm_generate'] = False

    # Filter out zero values
    valid_scores = filter_valid_scores(interactive_scores)

    if len(valid_scores) == 0:
        st.error("No capabilities scored. Please fill in at least one capability with both I and R values > 0.")
    else:
        with st.spinner("🔄 Generating report with parallel synthesis... This may take 30-60 seconds."):
            # Convert to analysis format
            scores_for_analysis = collect_scores_for_analysis(valid_scores)

            # Log activity
            log_user_activity(user, "generate_report", {"score_count": len(scores_for_analysis)})

            # Generate report with concurrent synthesis
            report_md = generate_report_concurrent(
                scores=scores_for_analysis,
                knowledge_base=kb,
                user_name=user['name'],
                max_workers=3
            )

            # Analyze for priority matrix
            analysis = analyze_capabilities(scores_for_analysis, kb)
            priority_matrix = create_priority_matrix(analysis)

            # Save to storage (save all scores, not just valid ones)
            assessment_id = save_assessment(user, interactive_scores, report_md)

            # Log completion
            log_user_activity(user, "report_complete", {"assessment_id": assessment_id})

            # Store in session state
            st.session_state['report'] = report_md
            st.session_state['analysis'] = analysis
            st.session_state['priority_matrix'] = priority_matrix
            st.session_state['assessment_id'] = assessment_id
            st.session_state['customer_context'] = {"user": user['name'], "email": user['email']}

        st.success(f"✅ Report generated and saved! (ID: {assessment_id})")
        st.rerun()


# ============================================================================
# REPORT DISPLAY
# ============================================================================
if 'report' in st.session_state:
    st.markdown("---")
    st.markdown("---")
    st.header("📋 Strategic Priority Guide")

    # Priority Matrix Visualization
    with st.expander("🎯 Priority Matrix Overview", expanded=True):
        pm = st.session_state['priority_matrix']

        cols = st.columns(6)
        categories = ["URGENT_GAP", "CRITICAL_GAP", "STRENGTH", "OPPORTUNITY", "MAINTAIN", "DEPRIORITIZE"]
        colors = ["🔴", "🟠", "🟢", "🟡", "🔵", "⚪"]

        for i, (cat, color) in enumerate(zip(categories, colors)):
            with cols[i]:
                count = pm.get(cat, 0)
                st.metric(cat.replace("_", " ").title(), f"{color} {count}")

    # Full Report
    st.markdown("""
    <style>
    /* Report paragraphs max width for better readability */
    .stMarkdown p {
        max-width: 600px;
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown(st.session_state['report'])

    # Export Options
    st.divider()
    st.header("📥 Export Report")

    col1, col2, col3 = st.columns(3)

    customer_ctx = st.session_state.get('customer_context', {})
    user_name = customer_ctx.get('user', 'Report').replace(' ', '_')

    with col1:
        docx_bytes = export_to_docx(st.session_state['report'], customer_ctx)
        st.download_button(
            label="📄 Download as DOCX",
            data=docx_bytes,
            file_name=f"O2C_Assessment_{user_name}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

    with col2:
        pdf_bytes = export_to_pdf(st.session_state['report'], customer_ctx)
        st.download_button(
            label="📑 Download as PDF",
            data=pdf_bytes,
            file_name=f"O2C_Assessment_{user_name}.pdf",
            mime="application/pdf"
        )

    with col3:
        md_content = export_to_markdown(st.session_state['report'], customer_ctx)
        st.download_button(
            label="📝 Download as Markdown",
            data=md_content,
            file_name=f"O2C_Assessment_{user_name}.md",
            mime="text/markdown"
        )
