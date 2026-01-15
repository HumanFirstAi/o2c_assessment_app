# CLAUDE.md - Fix Mobile Responsive Layout

## Problem

Mobile view is broken:
- All 8 phase headers render first (stacked vertically)
- Then all capability cards render separately
- Cards are NOT grouped under their respective phase headers

## Required Behavior

### Desktop (wide screen)
```
┌─────────┬─────────┬─────────┬─────────┬─────────┬─────────┬─────────┬─────────┐
│Configure│ Quote & │ Invoice │ Collect │Provision│Recognize│  Learn  │ Sustain │
├─────────┼─────────┼─────────┼─────────┼─────────┼─────────┼─────────┼─────────┤
│  Card   │  Card   │  Card   │  Card   │  Card   │  Card   │  Card   │  Card   │
│  Card   │  Card   │  Card   │  Card   │  Card   │  Card   │  Card   │  Card   │
└─────────┴─────────┴─────────┴─────────┴─────────┴─────────┴─────────┴─────────┘
```

### Mobile (narrow screen)
```
┌─────────────────────────┐
│   Configure and Price   │  ← Phase 1 header
├─────────────────────────┤
│ Offer/Catalog Mgmt   ℹ️ │  ← Phase 1 card 1
│   [I: 0]    [R: 0]      │
├─────────────────────────┤
│ Price Management     ℹ️ │  ← Phase 1 card 2
│   [I: 0]    [R: 0]      │
├─────────────────────────┤
│ Revenue Planning     ℹ️ │  ← Phase 1 card 3
│   [I: 0]    [R: 0]      │
├─────────────────────────┤
│ Incentive Mgmt       ℹ️ │  ← Phase 1 card 4
│   [I: 0]    [R: 0]      │
├─────────────────────────┤
│ Channel Management   ℹ️ │  ← Phase 1 card 5
│   [I: 0]    [R: 0]      │
└─────────────────────────┘

┌─────────────────────────┐
│     Quote and Sell      │  ← Phase 2 header
├─────────────────────────┤
│ Opportunity Capture  ℹ️ │  ← Phase 2 card 1
│   [I: 0]    [R: 0]      │
├─────────────────────────┤
│ Customer Portals     ℹ️ │  ← Phase 2 card 2
│   [I: 0]    [R: 0]      │
└─────────────────────────┘
... and so on for all 8 phases
```

---

## Solution: Render by PHASE, not by ROW

### Step 1: Add helper function to grid_layout.py

```python
def get_capabilities_by_phase(phase_id: str) -> list:
    """Get all non-empty capabilities for a specific phase, in order."""
    capabilities = []
    
    for row in GRID_LAYOUT:
        for cell in row:
            if not cell.get('empty') and cell.get('phase_id') == phase_id:
                capabilities.append(cell)
    
    return capabilities
```

### Step 2: Update render_assessment_grid in modules/interactive_form.py

```python
def render_assessment_grid():
    """
    Render assessment grid - responsive for desktop and mobile.
    Groups capabilities under their phase headers.
    """
    from grid_layout import PHASES, get_capabilities_by_phase
    
    for phase in PHASES:
        # Phase header (full width)
        st.markdown(f'''
        <div style="
            background: {phase['color']};
            color: {phase.get('text_color', 'white')};
            padding: 15px;
            text-align: center;
            border-radius: 8px;
            font-weight: bold;
            font-size: 14px;
            margin: 20px 0 10px 0;
        ">
            {phase['name']}
        </div>
        ''', unsafe_allow_html=True)
        
        # Get capabilities for THIS phase only
        phase_caps = get_capabilities_by_phase(phase['id'])
        
        # Render in responsive grid
        # On desktop: 2-3 cards per row within phase
        # On mobile: auto-stacks to 1 per row
        cols_per_row = 3
        
        for i in range(0, len(phase_caps), cols_per_row):
            row_caps = phase_caps[i:i + cols_per_row]
            cols = st.columns(len(row_caps), gap="small")
            
            for col_idx, cap in enumerate(row_caps):
                with cols[col_idx]:
                    render_capability_card(cap)
```

### Step 3: Update render_capability_card

```python
def render_capability_card(cell):
    """Render a single capability card with info button."""
    cap_id = cell['id']
    full_desc = get_capability_full_description(cap_id)
    
    with st.container(border=True):
        # Header: name + info button
        col1, col2 = st.columns([0.85, 0.15])
        
        with col1:
            st.markdown(f"**{cell['name']}**")
            st.caption(cell.get('subtitle', ''))
        
        with col2:
            with st.popover("ℹ️"):
                st.markdown(f"**{cell['name']}**")
                st.write(full_desc)
        
        # Score inputs - compact, side by side
        i_col, r_col = st.columns(2)
        with i_col:
            st.number_input("I", 0, 10, 0, key=f"i_{cap_id}", label_visibility="visible")
        with r_col:
            st.number_input("R", 0, 10, 0, key=f"r_{cap_id}", label_visibility="visible")
```

---

## Why Current Code is Wrong

### WRONG approach (current):
```python
# Renders ALL headers first, THEN all cards by row
phase_cols = st.columns(8)
for idx, phase in enumerate(PHASES):
    with phase_cols[idx]:
        render_header(phase)  # All 8 headers in one row

for row in GRID_LAYOUT:
    row_cols = st.columns(8)
    for col_idx, cell in enumerate(row):
        with row_cols[col_idx]:
            render_card(cell)  # Cards by row, not by phase
```

On mobile, st.columns stacks vertically, so you get:
1. Header 1, Header 2, Header 3... Header 8 (all stacked)
2. Row 1 Card 1, Row 1 Card 2... (all stacked)
3. Row 2 Card 1, Row 2 Card 2... (all stacked)

Cards are NOT grouped with their phase!

### CORRECT approach:
```python
# Renders each phase header followed by its cards
for phase in PHASES:
    render_header(phase)  # Phase 1 header
    
    phase_caps = get_capabilities_by_phase(phase['id'])
    for cap in phase_caps:
        render_card(cap)  # All Phase 1 cards
    
    # Loop continues to Phase 2 header, then Phase 2 cards, etc.
```

On mobile, this correctly shows:
1. Phase 1 Header
2. Phase 1 Card 1, Card 2, Card 3...
3. Phase 2 Header
4. Phase 2 Card 1, Card 2...

---

## Phase IDs Reference

Make sure these match in grid_layout.py:

```python
PHASES = [
    {"id": "configure_price", "name": "Configure and Price", "color": "#2E7D32"},
    {"id": "quote_sell", "name": "Quote and Sell", "color": "#1565C0"},
    {"id": "invoice", "name": "Invoice", "color": "#7B1FA2"},
    {"id": "collect", "name": "Collect", "color": "#00838F"},
    {"id": "provision", "name": "Provision", "color": "#F9A825", "text_color": "#333"},
    {"id": "recognize_report", "name": "Recognize and Report", "color": "#6A1B9A"},
    {"id": "learn", "name": "Learn", "color": "#EF6C00"},
    {"id": "sustain_grow", "name": "Sustain and Grow", "color": "#1976D2"},
]
```

Each capability in GRID_LAYOUT must have matching `phase_id`:

```python
{"id": "offer_catalog_management", "name": "Offer/Catalog Management", "phase_id": "configure_price", ...},
{"id": "opportunity_capture", "name": "Opportunity Capture", "phase_id": "quote_sell", ...},
```

---

## Testing

1. Desktop: Cards should display in grid under phase columns
2. Mobile: Resize browser narrow - each phase header should be followed by its cards
3. Verify: "Offer/Catalog Management" appears under "Configure and Price", not after all headers

---

## Summary

| Change | File |
|--------|------|
| Add `get_capabilities_by_phase()` | grid_layout.py |
| Rewrite `render_assessment_grid()` to loop by phase | modules/interactive_form.py |
| Keep `render_capability_card()` with info popover | modules/interactive_form.py |y

