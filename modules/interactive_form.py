import streamlit as st
import json
from datetime import datetime
from typing import Dict, List, Tuple
from grid_layout import GRID_LAYOUT, PHASES, get_all_capabilities, IMPORTANCE_STYLE, READINESS_STYLE, get_capability_full_description, get_capabilities_by_phase

def render_interactive_assessment(knowledge_base: dict) -> Dict:
    """
    Render the interactive 8x7 grid assessment matching the HTML template.
    Returns dict of scores keyed by capability_id.
    """

    # Initialize session state for scores
    if 'interactive_scores' not in st.session_state:
        st.session_state.interactive_scores = {}

    # Add custom CSS for the grid with responsive design
    st.markdown("""
    <div style="display: none;">
    <style type="text/css">
    /* Base styles */
    .grid-container {
        display: flex;
        flex-direction: column;
        gap: 2px;
    }
    .phase-header {
        text-align: center;
        font-weight: 600;
        font-size: 11px;
        padding: 8px 4px;
        border-radius: 3px;
        height: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
        white-space: pre-line;
        line-height: 1.2;
    }
    .capability-card {
        background: white !important;
        border: 2px solid #ddd;
        border-radius: 4px;
        padding: 8px;
        margin: 2px;
        height: 100px;
        min-height: 100px;
        max-height: 100px;
        overflow: hidden;
        font-size: 12px;
        color: #333 !important;
    }
    .empty-card {
        display: none;
    }
    .cap-name {
        font-weight: bold;
        font-size: 15px;
        margin-bottom: 4px;
        line-height: 1.3;
        color: #333 !important;
    }
    .cap-subtitle {
        font-style: italic;
        color: #888 !important;
        font-size: 12px;
        margin-bottom: 5px;
    }
    .score-label-i {
        font-size: 10px;
        font-weight: bold;
        color: #E6007E;
    }
    .score-label-r {
        font-size: 10px;
        font-weight: bold;
        color: #00A5A8;
    }

    /* Priority border colors */
    .priority-urgent {
        border-color: #dc3545 !important;
        border-width: 3px !important;
    }
    .priority-critical {
        border-color: #fd7e14 !important;
        border-width: 3px !important;
    }
    .priority-strength {
        border-color: #28a745 !important;
        border-width: 3px !important;
    }
    .priority-opportunity {
        border-color: #ffc107 !important;
        border-width: 2px !important;
    }

    /* Input styling - larger touch targets on mobile */
    .stNumberInput input {
        font-size: 14px;
        text-align: center;
        padding: 8px;
        min-height: 44px;
    }

    /* Compact input container */
    .compact-input-container {
        max-width: 280px;
        margin: 8px 0 16px 0;
    }

    /* Responsive adjustments */
    @media (max-width: 768px) {
        /* Mobile styles */
        .phase-header {
            font-size: 14px;
            height: auto;
            min-height: 60px;
            padding: 12px 8px;
        }
        .capability-card {
            height: auto;
            min-height: 120px;
            max-height: none;
            padding: 12px;
            font-size: 15px;
        }
        .cap-name {
            font-size: 14px;
            margin-bottom: 8px;
        }
        .cap-subtitle {
            font-size: 12px;
            margin-bottom: 8px;
        }
        .score-label-i,
        .score-label-r {
            font-size: 14px;
            margin-bottom: 4px;
        }
        .stNumberInput input {
            font-size: 16px;
            padding: 12px;
            min-height: 48px;
        }
        /* Stack columns on mobile */
        [data-testid="column"] {
            min-width: 100% !important;
            flex: 1 1 100% !important;
        }
        /* Make sidebar full width on mobile */
        [data-testid="stSidebar"] {
            min-width: 100% !important;
        }
    }

    @media (min-width: 769px) and (max-width: 1024px) {
        /* Tablet styles */
        .phase-header {
            font-size: 10px;
            padding: 6px 4px;
        }
        .capability-card {
            font-size: 10px;
            padding: 10px;
        }
        .cap-name {
            font-size: 12px;
        }
        .cap-subtitle {
            font-size: 10px;
        }
    }

    @media (min-width: 1025px) {
        /* Desktop styles - original sizes */
        .stNumberInput input {
            padding: 4px;
        }
    }

    /* Make buttons full width on mobile */
    @media (max-width: 768px) {
        .stButton button {
            width: 100%;
            min-height: 48px;
            font-size: 16px;
        }
        .stDownloadButton button {
            width: 100%;
            min-height: 48px;
            font-size: 16px;
        }
    }
    </style>
    </div>
    """, unsafe_allow_html=True)

    # Score guide header
    st.markdown("""
    ### 📊 Score Guide
    """)

    st.markdown("""
    <style>
    .score-guide-container {
        display: flex;
        gap: 20px;
        margin-bottom: 20px;
    }
    .score-guide-box {
        flex: 1;
        border-radius: 8px;
        padding: 15px;
    }
    .score-guide-title {
        font-weight: 600;
        font-size: 16px;
    }
    .score-guide-desc {
        font-size: 12px;
        margin-top: 4px;
    }

    @media (max-width: 768px) {
        .score-guide-container {
            flex-direction: column;
            gap: 12px;
        }
        .score-guide-box {
            padding: 20px;
        }
        .score-guide-title {
            font-size: 18px;
        }
        .score-guide-desc {
            font-size: 14px;
            margin-top: 8px;
        }
    }
    </style>
    <div class="score-guide-container">
        <div class="score-guide-box" style="background: #fce4ec; border: 2px dashed #E6007E;">
            <div class="score-guide-title" style="color: #E6007E;">
                I = Importance/Impact
            </div>
            <div class="score-guide-desc" style="color: #666;">
                1 = Low Impact → 10 = Mission Critical
            </div>
        </div>
        <div class="score-guide-box" style="background: #e0f7fa; border: 2px dashed #00A5A8;">
            <div class="score-guide-title" style="color: #00838F;">
                R = Strategic Readiness
            </div>
            <div class="score-guide-desc" style="color: #555;">
                1 = Not Ready → 10 = Fully Capable
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Mobile-responsive layout: group by phase
    # On desktop: shows multiple columns, on mobile: stacks vertically
    for phase in PHASES:
        # Phase header (full width)
        st.markdown(f'''
        <div style="
            background: {phase['color']};
            color: {phase.get('text_color', 'white')};
            padding: 14px;
            text-align: center;
            border-radius: 8px;
            font-weight: 600;
            font-size: 15px;
            margin: 24px 0 12px 0;
        ">
            {phase['name']}
        </div>
        ''', unsafe_allow_html=True)

        # Get capabilities for this phase
        capabilities = get_capabilities_by_phase(phase['id'])

        # Render cards in responsive columns
        # Desktop: 3-4 cards per row, Mobile: stacks automatically
        for cap in capabilities:
            render_capability_card(cap, 0, 0, knowledge_base)

    # Feedback loop footer
    st.markdown("---")
    st.markdown("""
    <div style="background: linear-gradient(90deg, #1976D2 0%, #00838F 25%, #F9A825 50%, #EF6C00 75%, #2E7D32 100%);
                color: white; padding: 10px; border-radius: 20px; text-align: center; margin-top: 20px;">
        <strong>Continuous Feedback Loop:</strong> Sustain & Grow → Configure & Price → Quote & Sell → Invoice → Collect → Provision → Recognize & Report → Learn
    </div>
    """, unsafe_allow_html=True)

    return st.session_state.interactive_scores


def render_capability_card(cell: Dict, row_idx: int, col_idx: int, knowledge_base: dict):
    """Render a single capability card with I/R inputs."""
    cap_id = cell["id"]

    # Get current scores (default to 0 - empty/not scored)
    current_scores = st.session_state.interactive_scores.get(cap_id, {"importance": 0, "readiness": 0})

    # Determine priority border color
    priority_class = get_priority_class(current_scores["importance"], current_scores["readiness"])
    border_colors = {
        "priority-urgent": "#dc3545",
        "priority-critical": "#fd7e14",
        "priority-strength": "#28a745",
        "priority-opportunity": "#ffc107",
        "": "#ddd"
    }
    border_color = border_colors.get(priority_class, "#ddd")
    border_width = "3px" if priority_class in ["priority-urgent", "priority-critical", "priority-strength"] else "2px"

    # Build subtitle HTML if exists - as a single complete string
    subtitle_html = ""
    if cell.get("subtitle"):
        subtitle_html = f'''<div style="
            font-size: 12px;
            color: #888;
            font-style: italic;
            line-height: 1.2;
            margin-top: 4px;
            overflow: hidden;
            text-overflow: ellipsis;
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
        ">{cell["subtitle"]}</div>'''

    # Get full description for hover tooltip
    full_desc = get_capability_full_description(cap_id)
    # Escape HTML entities and newlines for inline HTML
    full_desc_escaped = full_desc.replace('"', '&quot;').replace("'", "&#39;").replace('\n', ' ')

    # Unique ID for this card
    card_id = f"card_{cap_id}"

    # Build card HTML with hover tooltip
    card_html = f'''
    <div class="capability-card-hover" id="{card_id}" style="
        position: relative;
        cursor: pointer;
        margin-bottom: 4px;
    ">
        <div style="
            background: white;
            border: {border_width} solid {border_color};
            border-radius: 6px;
            padding: 10px;
            height: 100px;
            min-height: 100px;
            max-height: 100px;
            min-width: 140px;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
        ">
            <div style="
                font-weight: 600;
                font-size: 15px;
                color: #333;
                line-height: 1.2;
                margin-bottom: 4px;
                overflow: hidden;
                text-overflow: ellipsis;
                display: -webkit-box;
                -webkit-line-clamp: 2;
                -webkit-box-orient: vertical;
            ">
                {cell["name"]}
            </div>
            {subtitle_html}
        </div>

        <!-- Tooltip - appears after 1s hover -->
        <div class="card-tooltip" style="
            visibility: hidden;
            opacity: 0;
            position: absolute;
            top: 105%;
            left: 0;
            width: 300px;
            max-width: 90vw;
            padding: 14px;
            background: #1a1a1a;
            color: #fff;
            border-radius: 8px;
            font-size: 12px;
            font-weight: normal;
            line-height: 1.6;
            z-index: 9999;
            box-shadow: 0 6px 20px rgba(0,0,0,0.5);
            transition: visibility 0s linear 1s, opacity 0.3s ease 1s;
        ">
            <div style="font-weight: 600; font-size: 13px; margin-bottom: 8px;">{cell["name"]}</div>
            <div style="font-size: 11px; line-height: 1.5;">{full_desc_escaped}</div>
        </div>
    </div>
    '''

    # Compact container with max-width for mobile
    with st.container():
        # Render card (no separate info column needed)
        st.markdown(card_html, unsafe_allow_html=True)

        # Compact inputs with max-width and spacers
        st.markdown('<div style="max-width: 280px; margin: 8px 0 16px 0;">', unsafe_allow_html=True)

        # Score inputs in two columns (compact)
        spacer1, input_col1, input_col2, spacer2 = st.columns([0.05, 0.4, 0.4, 0.15])

        with input_col1:
            st.markdown(f'<div class="score-label-i" style="font-size: 11px; font-weight: bold; color: #E6007E; margin-bottom: 2px;">I</div>', unsafe_allow_html=True)
            i_score = st.number_input(
                "Importance",
                min_value=0,
                max_value=10,
                value=current_scores["importance"],
                key=f"i_{cap_id}_{row_idx}_{col_idx}",
                label_visibility="collapsed"
            )

        with input_col2:
            st.markdown(f'<div class="score-label-r" style="font-size: 11px; font-weight: bold; color: #00838F; margin-bottom: 2px;">R</div>', unsafe_allow_html=True)
            r_score = st.number_input(
                "Readiness",
                min_value=0,
                max_value=10,
                value=current_scores["readiness"],
                key=f"r_{cap_id}_{row_idx}_{col_idx}",
                label_visibility="collapsed"
            )

        st.markdown('</div>', unsafe_allow_html=True)

    # Update session state
    st.session_state.interactive_scores[cap_id] = {
        "importance": i_score,
        "readiness": r_score,
        "phase_id": cell["phase_id"]
    }


def get_priority_class(importance: int, readiness: int) -> str:
    """Return CSS class based on priority category."""
    if importance >= 7 and readiness <= 4:
        return "priority-urgent"
    elif importance >= 7 and readiness <= 6:
        return "priority-critical"
    elif importance >= 7 and readiness >= 7:
        return "priority-strength"
    elif importance <= 3:
        return ""  # No special highlighting for deprioritize
    else:
        return "priority-opportunity"


def get_capability_tooltip(cap_id: str, knowledge_base: dict) -> str:
    """Get tooltip content for a capability from knowledge base."""
    # Find capability in knowledge base
    for phase in knowledge_base.get("phases", []):
        for cap in phase.get("capabilities", []):
            if cap.get("id") == cap_id:
                agents = cap.get("agent_mapping", {}).get("primary_agents", [])
                timeline = cap.get("whats_coming", {}).get("timeline", "")
                why = cap.get("why_it_matters", "")[:150]

                tooltip = f"Why it matters: {why}..."
                if agents:
                    tooltip += f"\n\nAI Agents: {', '.join(agents[:3])}"
                if timeline:
                    tooltip += f"\n\nTimeline: {timeline}"

                return tooltip

    return "No additional context available"


def render_progress_sidebar(scores: Dict):
    """Show assessment completion progress in sidebar."""
    # Use actual number of scores being tracked
    total_capabilities = len(scores) if scores else 42

    # Count non-default scores (assuming default is 5,5)
    completed = sum(1 for cap_id, data in scores.items()
                    if data["importance"] != 5 or data["readiness"] != 5)

    # Ensure progress doesn't exceed 1.0
    progress_value = min(completed / total_capabilities, 1.0) if total_capabilities > 0 else 0

    st.sidebar.metric("Assessment Progress", f"{completed}/{total_capabilities}")
    st.sidebar.progress(progress_value)

    # Calculate urgent gaps
    urgent_count = sum(1 for cap_id, data in scores.items()
                      if data["importance"] >= 7 and data["readiness"] <= 4)

    if urgent_count > 0:
        st.sidebar.warning(f"⚠️ {urgent_count} Urgent Gaps Identified")

    # Phase-level summary
    st.sidebar.subheader("Phase Summary")
    for phase in PHASES:
        phase_caps = [cap_id for cap_id, data in scores.items()
                     if data.get("phase_id") == phase["id"]]
        if phase_caps:
            phase_urgent = sum(1 for cap_id in phase_caps
                             if scores[cap_id]["importance"] >= 7
                             and scores[cap_id]["readiness"] <= 4)

            icon = "🔴" if phase_urgent > 0 else "🟢"
            st.sidebar.write(f"{icon} {phase['name'].replace(chr(10), ' ')}: {phase_urgent} urgent")


def save_assessment_json(scores: Dict, customer_context: Dict) -> str:
    """Export current scores as JSON for save/load."""
    data = {
        "version": "1.0",
        "timestamp": datetime.now().isoformat(),
        "customer": customer_context,
        "scores": scores,
        "total_capabilities": len(scores)
    }
    return json.dumps(data, indent=2)


def load_assessment_json(json_data: str) -> Tuple[Dict, Dict]:
    """Load scores from JSON. Returns (scores, customer_context)."""
    try:
        data = json.loads(json_data)
        return data.get("scores", {}), data.get("customer", {})
    except json.JSONDecodeError:
        return {}, {}


def collect_scores_for_analysis(scores: Dict) -> List[Dict]:
    """
    Convert session state scores to format expected by score_analyzer.
    Returns list of dicts with capability_id, phase_id, importance, readiness.
    """
    result = []
    for cap_id, data in scores.items():
        result.append({
            "capability_id": cap_id,
            "phase_id": data.get("phase_id", ""),
            "importance": data["importance"],
            "readiness": data["readiness"]
        })
    return result
