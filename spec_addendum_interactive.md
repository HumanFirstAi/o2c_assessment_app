# SPEC ADDENDUM: Interactive Assessment Form

## Overview

This addendum extends the original spec to include:
1. **Interactive digital form** - An online version matching the HTML template layout
2. **Image upload** - Keep the existing OCR/vision approach as alternative input method
3. **Grid layout mapping** - Exact cell positions for the 8x7 grid

---

## 1. GRID LAYOUT MAPPING

The assessment is an 8-column (phases) × 7-row grid. Each cell is either a capability or empty.

### Grid Structure

```
Column:     1              2              3              4              5              6              7              8
Phase:      Configure      Quote          Invoice        Collect        Provision      Recognize      Learn          Sustain
            & Price        & Sell                                                      & Report                      & Grow
Color:      #2E7D32        #1565C0        #7B1FA2        #00838F        #F9A825        #6A1B9A        #EF6C00        #1976D2
```

### Cell Mapping (capability_id or "empty")

```python
GRID_LAYOUT = [
    # Row 1
    [
        {"id": "offer_catalog_management", "name": "Offer/Catalog Management", "subtitle": "Price, Usage, Promo"},
        {"id": "opportunity_capture", "name": "Opportunity Capture", "subtitle": "eCommerce, CRM, Partners"},
        {"id": "order_management", "name": "Order Management", "subtitle": None},
        {"id": "payment_routing", "name": "Payment and Routing", "subtitle": None},
        {"id": "entitlement_management", "name": "Entitlement Management", "subtitle": None},
        {"id": "revenue_recognition", "name": "Revenue Recognition", "subtitle": None},
        {"id": "revenue_profit_insights", "name": "Revenue and Profit Insights", "subtitle": None},
        {"id": "churn_prevent", "name": "Churn Prevention", "subtitle": "Win-back Offers"},
    ],
    # Row 2
    [
        {"id": "price_management", "name": "Price Management", "subtitle": None},
        {"id": "customer_partner_portals", "name": "Customer and Partner Portals", "subtitle": None},
        {"id": "billing_invoice", "name": "Billing, Invoice", "subtitle": None},
        {"id": "customer_credit_management", "name": "Customer Credit Management", "subtitle": None},
        {"id": "inventory", "name": "Inventory", "subtitle": None},
        {"id": "accounting_ledger", "name": "Accounting Ledger", "subtitle": None},
        {"id": "customer_insights", "name": "Customer Insights", "subtitle": "Churn Detect"},
        {"id": "renewals", "name": "Renewals", "subtitle": "CPQ, Upsell/Cross-sell"},
    ],
    # Row 3
    [
        {"id": "revenue_planning", "name": "Revenue Planning", "subtitle": None},
        {"id": "guided_selling", "name": "Guided Selling", "subtitle": "CPQ, Price Guidance"},
        {"id": "rating_charging", "name": "Rating and Charging", "subtitle": None},
        {"id": "dunning_payment_retry", "name": "Dunning and Payment Retry", "subtitle": None},
        {"id": "fulfillment_ship", "name": "Fulfillment and Ship", "subtitle": None},
        {"id": "usage_entitlement_enforcement", "name": "Usage and Entitlement Enforcement", "subtitle": None},
        {"id": "offer_insights", "name": "Offer Insights", "subtitle": None},
        {"id": "customer_success", "name": "Customer Success", "subtitle": "Health, Education"},
    ],
    # Row 4
    [
        {"id": "incentive_management", "name": "Incentive Management", "subtitle": "Rebates, Discounts"},
        {"id": "customer_risk_fraud", "name": "Customer Risk and Fraud Check", "subtitle": None},
        {"id": "usage_data_mediation", "name": "Usage Data Mediation", "subtitle": None},
        {"id": "collections", "name": "Collections", "subtitle": None},
        {"id": "deployment_provisioning", "name": "Deployment / Provisioning", "subtitle": None},
        {"id": "reporting_dashboards", "name": "Reporting and Dashboards", "subtitle": None},
        {"id": "customer_value_intelligence", "name": "Customer Value Intelligence", "subtitle": "Transactions, Usage, Risk"},
        {"id": "empty", "name": "—", "subtitle": None},
    ],
    # Row 5
    [
        {"id": "channel_management", "name": "Channel Management", "subtitle": None},
        {"id": "contract_management", "name": "Contract Management", "subtitle": None},
        {"id": "anomaly_detection", "name": "Anomaly Detection", "subtitle": None},
        {"id": "partner_settlement", "name": "Partner Settlement", "subtitle": "Incentives and Payment"},
        {"id": "empty", "name": "—", "subtitle": None},
        {"id": "tax", "name": "Tax", "subtitle": None},
        {"id": "price_profit_optimization", "name": "Price/Profit Optimization", "subtitle": None},
        {"id": "empty", "name": "—", "subtitle": None},
    ],
    # Row 6
    [
        {"id": "empty", "name": "—", "subtitle": None},
        {"id": "inventory_ship_availability", "name": "Inventory/Ship Availability", "subtitle": None},
        {"id": "dispute_prediction", "name": "Dispute Prediction", "subtitle": None},
        {"id": "empty", "name": "—", "subtitle": None},
        {"id": "empty", "name": "—", "subtitle": None},
        {"id": "compliance", "name": "Compliance", "subtitle": None},
        {"id": "partner_channel_intelligence", "name": "Partner/Channel Intelligence", "subtitle": None},
        {"id": "empty", "name": "—", "subtitle": None},
    ],
    # Row 7
    [
        {"id": "empty", "name": "—", "subtitle": None},
        {"id": "empty", "name": "—", "subtitle": None},
        {"id": "empty", "name": "—", "subtitle": None},
        {"id": "empty", "name": "—", "subtitle": None},
        {"id": "empty", "name": "—", "subtitle": None},
        {"id": "empty", "name": "—", "subtitle": None},
        {"id": "benchmarks", "name": "Benchmarks", "subtitle": None},
        {"id": "empty", "name": "—", "subtitle": None},
    ],
]
```

### Phase Definitions

```python
PHASES = [
    {"id": "configure_price", "name": "Configure\nand Price", "color": "#2E7D32", "text_color": "white"},
    {"id": "quote_sell", "name": "Quote and\nSell", "color": "#1565C0", "text_color": "white"},
    {"id": "invoice", "name": "Invoice", "color": "#7B1FA2", "text_color": "white"},
    {"id": "collect", "name": "Collect", "color": "#00838F", "text_color": "white"},
    {"id": "provision", "name": "Provision", "color": "#F9A825", "text_color": "#333"},
    {"id": "recognize_report", "name": "Recognize\nand Report", "color": "#6A1B9A", "text_color": "white"},
    {"id": "learn", "name": "Learn", "color": "#EF6C00", "text_color": "white"},
    {"id": "sustain_grow", "name": "Sustain\nand Grow", "color": "#1976D2", "text_color": "white"},
]
```

---

## 2. INTERACTIVE FORM REQUIREMENTS

### 2.1 Visual Design

The interactive form MUST match the HTML template exactly:

**Layout:**
- 8 columns (one per phase)
- 7 rows of capability cards
- Phase headers with correct colors
- Empty cells shown as grayed out (no input)

**Capability Card Design:**
- White background with light gray border
- Capability name (bold, 8-10px)
- Subtitle in italic gray (if present)
- Two input fields side by side:
  - I (Importance): Pink background (#fce4ec), pink dashed border (#E6007E)
  - R (Readiness): Cyan background (#e0f7fa), teal dashed border (#00A5A8)

**Score Guide Header:**
- Pink box with "I" = Importance/Impact (1=Low → 10=Critical)
- Teal box with "R" = Strategic Readiness (1=Not ready → 10=Fully capable)
- Priority Matrix explanation

**Feedback Loop Footer:**
- Gradient pill showing cycle from Sustain→Configure

### 2.2 Streamlit Implementation

```python
# app.py - Interactive Assessment Tab

import streamlit as st
from grid_layout import GRID_LAYOUT, PHASES

def render_interactive_assessment():
    """Render the interactive assessment form matching the HTML template."""
    
    st.markdown("""
    <style>
    .phase-header {
        text-align: center;
        color: white;
        font-weight: 600;
        font-size: 11px;
        padding: 8px 4px;
        height: 45px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .capability-card {
        background: white;
        border: 1px solid #ddd;
        border-radius: 3px;
        padding: 5px;
        margin: 2px;
        min-height: 70px;
    }
    .empty-card {
        background: #fafafa;
        border: 1px solid #eee;
    }
    .score-input-i {
        background: #fce4ec;
        border: 1px dashed #E6007E;
    }
    .score-input-r {
        background: #e0f7fa;
        border: 1px dashed #00A5A8;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state for scores
    if 'scores' not in st.session_state:
        st.session_state.scores = {}
    
    # Render phase headers
    header_cols = st.columns(8)
    for i, phase in enumerate(PHASES):
        with header_cols[i]:
            st.markdown(
                f'<div class="phase-header" style="background-color: {phase["color"]}; color: {phase["text_color"]}">'
                f'{phase["name"]}</div>',
                unsafe_allow_html=True
            )
    
    # Render grid rows
    for row_idx, row in enumerate(GRID_LAYOUT):
        cols = st.columns(8)
        for col_idx, cell in enumerate(row):
            with cols[col_idx]:
                if cell["id"] == "empty":
                    st.markdown('<div class="capability-card empty-card"><center>—</center></div>', 
                                unsafe_allow_html=True)
                else:
                    render_capability_card(cell, row_idx, col_idx)

def render_capability_card(cell, row_idx, col_idx):
    """Render a single capability card with I/R inputs."""
    cap_id = cell["id"]
    
    # Card container
    with st.container():
        st.markdown(f"**{cell['name']}**")
        if cell["subtitle"]:
            st.caption(cell["subtitle"])
        
        # Score inputs
        score_cols = st.columns(2)
        with score_cols[0]:
            i_score = st.number_input(
                "I",
                min_value=1, max_value=10, value=5,
                key=f"i_{cap_id}",
                label_visibility="collapsed"
            )
        with score_cols[1]:
            r_score = st.number_input(
                "R",
                min_value=1, max_value=10, value=5,
                key=f"r_{cap_id}",
                label_visibility="collapsed"
            )
        
        # Store in session state
        st.session_state.scores[cap_id] = {
            "importance": i_score,
            "readiness": r_score
        }
```

### 2.3 Two Input Modes

The app should support TWO input methods on separate tabs:

**Tab 1: Interactive Form**
- Digital version of the assessment
- User clicks/types scores directly
- Real-time validation
- Can hover over capability for AI context tooltip
- Save/load progress
- Export as JSON

**Tab 2: Upload Image**
- Upload completed paper assessment
- Use Claude Vision to extract scores
- Show extracted scores for verification/editing
- Same downstream analysis

```python
# Main app structure
tab1, tab2 = st.tabs(["📝 Interactive Assessment", "📤 Upload Completed Form"])

with tab1:
    render_interactive_assessment()
    if st.button("Generate Report", key="interactive_report"):
        scores = collect_scores_from_form()
        generate_report(scores)

with tab2:
    uploaded_file = st.file_uploader("Upload assessment image", type=["png", "jpg", "pdf"])
    if uploaded_file:
        extracted_scores = extract_scores_from_image(uploaded_file)
        display_extracted_scores_for_review(extracted_scores)
        if st.button("Generate Report", key="upload_report"):
            generate_report(extracted_scores)
```

---

## 3. ENHANCED FEATURES FOR INTERACTIVE MODE

### 3.1 Capability Tooltips

When user hovers over a capability, show AI context from knowledge base:

```python
def get_capability_tooltip(cap_id: str, knowledge_base: dict) -> str:
    """Get tooltip content for a capability."""
    cap_data = find_capability_in_kb(cap_id, knowledge_base)
    if not cap_data:
        return ""
    
    return f"""
    **Why it matters:** {cap_data['why_it_matters'][:200]}...
    
    **AI Agents Available:** {', '.join(cap_data['agent_mapping']['primary_agents'])}
    
    **Timeline:** {cap_data['whats_coming']['timeline']}
    """
```

### 3.2 Real-Time Priority Highlighting

As users enter scores, highlight the card based on priority:

```python
def get_priority_color(importance: int, readiness: int) -> str:
    """Return border color based on priority category."""
    if importance >= 7 and readiness <= 4:
        return "#dc3545"  # Red - Urgent Gap
    elif importance >= 7 and readiness <= 6:
        return "#fd7e14"  # Orange - Critical Gap
    elif importance >= 7 and readiness >= 7:
        return "#28a745"  # Green - Strength
    elif importance <= 3:
        return "#6c757d"  # Gray - Deprioritize
    else:
        return "#ffc107"  # Yellow - Opportunity/Maintain
```

### 3.3 Progress Tracking

Show completion percentage and phase-level summary:

```python
def render_progress_sidebar():
    """Show assessment completion progress."""
    total_capabilities = 38  # Non-empty cells
    completed = sum(1 for cap_id, scores in st.session_state.scores.items() 
                    if scores["importance"] != 5 or scores["readiness"] != 5)
    
    st.sidebar.metric("Completion", f"{completed}/{total_capabilities}")
    st.sidebar.progress(completed / total_capabilities)
    
    # Phase-level summary
    st.sidebar.subheader("Phase Summary")
    for phase in PHASES:
        phase_caps = get_capabilities_for_phase(phase["id"])
        urgent_count = sum(1 for c in phase_caps 
                          if is_urgent_gap(st.session_state.scores.get(c["id"], {})))
        st.sidebar.write(f"{phase['name']}: {urgent_count} urgent gaps")
```

### 3.4 Save/Load Assessment

Allow users to save progress and reload:

```python
def save_assessment():
    """Export current scores as JSON."""
    data = {
        "timestamp": datetime.now().isoformat(),
        "customer": st.session_state.get("company_name", ""),
        "scores": st.session_state.scores
    }
    return json.dumps(data, indent=2)

def load_assessment(json_data: str):
    """Load scores from JSON."""
    data = json.loads(json_data)
    st.session_state.scores = data["scores"]
    st.session_state.company_name = data.get("customer", "")
```

---

## 4. VISION EXTRACTION PROMPT UPDATE

Update the extraction prompt to match the exact grid layout:

```python
EXTRACTION_PROMPT = """
Analyze this Recurring Revenue Management Lifecycle Assessment image.

The assessment is an 8-column × 7-row grid with these phases (left to right):
1. Configure and Price (green header)
2. Quote and Sell (blue header)
3. Invoice (purple header)
4. Collect (teal header)
5. Provision (yellow header)
6. Recognize and Report (dark purple header)
7. Learn (orange header)
8. Sustain and Grow (blue header)

For each capability card (white boxes with I:___ and R:___ fields), extract:
- Row number (1-7)
- Column number (1-8)
- Capability name (the bold text)
- I score (Importance, 1-10) - look for handwritten or typed number after "I:"
- R score (Readiness, 1-10) - look for handwritten or typed number after "R:"

Skip cells that show only "—" (these are empty placeholder cells).

Return as JSON:
{
  "scores": [
    {"row": 1, "col": 1, "capability": "Offer/Catalog Management", "importance": 8, "readiness": 3},
    {"row": 1, "col": 2, "capability": "Opportunity Capture", "importance": 7, "readiness": 5},
    ...
  ],
  "confidence": "high|medium|low",
  "notes": "Any legibility issues or uncertainties"
}

Use null for any score that cannot be read clearly.
"""
```

---

## 5. FILE STRUCTURE UPDATE

```
o2c_assessment_app/
├── app.py                      # Main app with tabs for both input modes
├── requirements.txt
├── config.py
├── knowledge_base.json         # Full AI/MCP context
├── grid_layout.py              # Grid mapping from this spec
├── modules/
│   ├── __init__.py
│   ├── interactive_form.py     # Interactive assessment renderer
│   ├── image_processor.py      # Vision-based extraction
│   ├── score_analyzer.py       # Priority analysis
│   ├── report_generator.py     # LLM report generation
│   └── export_handler.py       # DOCX/PDF/JSON export
├── templates/
│   ├── lifecycle_assessment.html  # Original template for reference
│   └── styles.css
└── assets/
    └── sample_completed.png    # Sample for testing
```

---

## 6. CAPABILITY COUNT VERIFICATION

**Active capabilities (require I/R scores): 38**

| Phase | Count | Capabilities |
|-------|-------|--------------|
| Configure & Price | 5 | Offer/Catalog, Price Mgmt, Revenue Planning, Incentive Mgmt, Channel Mgmt |
| Quote & Sell | 6 | Opportunity, Portals, Guided Selling, Risk/Fraud, Contract, Inventory/Ship |
| Invoice | 6 | Order Mgmt, Billing/Invoice, Rating, Usage Mediation, Anomaly, Dispute |
| Collect | 5 | Payment/Routing, Credit Mgmt, Dunning, Collections, Partner Settlement |
| Provision | 4 | Entitlement, Inventory, Fulfillment, Deployment |
| Recognize & Report | 6 | Revenue Rec, Accounting, Usage Enforcement, Reporting, Tax, Compliance |
| Learn | 7 | Rev/Profit Insights, Customer Insights, Offer Insights, CVI, Price Opt, Channel Intel, Benchmarks |
| Sustain & Grow | 3 | Churn Prevention, Renewals, Customer Success |

**Empty cells: 18** (shown as "—" in the grid)

---

## 7. UPDATED CLAUDE.md INSTRUCTIONS

Add this to CLAUDE.md:

```markdown
## Interactive Form Feature

The app has TWO input methods:

### Tab 1: Interactive Assessment
- Render the grid exactly matching `lifecycle_assessment.html`
- Use `grid_layout.py` for cell positions
- 8 columns (phases) × 7 rows
- Each capability card has I and R number inputs (1-10)
- Empty cells (id="empty") are grayed out, no inputs
- Real-time priority highlighting based on I/R values
- Tooltips showing AI agent context from knowledge_base.json
- Progress tracking in sidebar
- Save/Load assessment as JSON

### Tab 2: Upload Image
- Accept PNG/JPG/PDF of completed paper form
- Use Claude Vision to extract scores
- Map extracted data to grid layout
- Allow user to verify/edit before analysis

### Both tabs lead to same report generation
```

---

*Spec Addendum v1.0 | Grid Layout + Interactive Form*
