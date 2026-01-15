# CLAUDE.md - Fix Desktop UI Layout

## Problems

1. App is full width - needs max-width 1000px
2. White capability cards are inconsistent sizes
3. Info button (ℹ️) is separate/floating - should be inside the card
4. Score inputs are disconnected from their cards

## Target Layout

```
┌──────────────────────────── max-width: 1000px ────────────────────────────┐
│                                                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │                      Configure and Price                             │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                            │
│  ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐          │
│  │ Offer/Catalog  ℹ️│ │ Price Mgmt     ℹ️│ │ Revenue Plan   ℹ️│          │
│  │ Managing price...│ │ Standardizing...│ │ Projecting...   │          │
│  │ [I: 0]   [R: 0] │ │ [I: 0]   [R: 0] │ │ [I: 0]   [R: 0] │          │
│  └──────────────────┘ └──────────────────┘ └──────────────────┘          │
│        180px               180px               180px                      │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## Fix 1: Add Global Max Width

**In app.py, add at the top after st.set_page_config:**

```python
st.markdown("""
<style>
/* Constrain app width */
.main .block-container {
    max-width: 1000px;
    padding-left: 2rem;
    padding-right: 2rem;
    margin: 0 auto;
}

/* Center the content */
.stApp {
    display: flex;
    justify-content: center;
}
</style>
""", unsafe_allow_html=True)
```

---

## Fix 2: Consistent Card Sizes with Info Button Inside

**Update render_capability_card in modules/interactive_form.py:**

```python
def render_capability_card(cell):
    """Render capability card with fixed width and integrated info button."""
    cap_id = cell['id']
    full_desc = get_capability_full_description(cap_id)
    
    # Single container for entire card including inputs
    st.markdown(f'''
    <style>
    .capability-card-wrapper {{
        width: 100%;
        max-width: 200px;
        min-width: 160px;
    }}
    </style>
    ''', unsafe_allow_html=True)
    
    # Card with info button INSIDE
    with st.container(border=True):
        # Row 1: Title and info button on same line
        st.markdown(f'''
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 4px;">
            <span style="font-weight: 600; font-size: 13px; color: #333; flex: 1;">
                {cell['name']}
            </span>
        </div>
        <div style="font-size: 11px; color: #888; font-style: italic; margin-bottom: 8px;">
            {cell.get('subtitle', '')}
        </div>
        ''', unsafe_allow_html=True)
        
        # Info button (small, aligned right)
        with st.popover("ℹ️ Info"):
            st.markdown(f"**{cell['name']}**")
            st.divider()
            st.write(full_desc)
        
        # Score inputs INSIDE the card container
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("I", 0, 10, 0, key=f"i_{cap_id}", label_visibility="visible")
        with col2:
            st.number_input("R", 0, 10, 0, key=f"r_{cap_id}", label_visibility="visible")
```

---

## Fix 3: Better Grid Layout with Fixed Widths

**Update render_assessment_grid in modules/interactive_form.py:**

```python
def render_assessment_grid():
    """Render assessment grid with consistent card sizes."""
    from grid_layout import PHASES, get_capabilities_by_phase
    
    for phase in PHASES:
        # Phase header
        st.markdown(f'''
        <div style="
            background: {phase['color']};
            color: {phase.get('text_color', 'white')};
            padding: 15px;
            text-align: center;
            border-radius: 8px;
            font-weight: bold;
            font-size: 14px;
            margin: 25px 0 15px 0;
        ">
            {phase['name']}
        </div>
        ''', unsafe_allow_html=True)
        
        # Get capabilities for this phase
        phase_caps = get_capabilities_by_phase(phase['id'])
        
        # Fixed 5 columns for desktop (will stack on mobile)
        cols_per_row = 5
        
        for i in range(0, len(phase_caps), cols_per_row):
            row_caps = phase_caps[i:i + cols_per_row]
            
            # Create equal-width columns
            cols = st.columns(cols_per_row, gap="small")
            
            for col_idx, cap in enumerate(row_caps):
                with cols[col_idx]:
                    render_capability_card(cap)
            
            # Fill empty columns if row is incomplete (keeps alignment)
            # Empty columns are already created, just not filled
```

---

## Fix 4: CSS for Consistent Card Dimensions

**Add to app.py global styles:**

```python
st.markdown("""
<style>
/* App max width */
.main .block-container {
    max-width: 1000px;
    margin: 0 auto;
}

/* Consistent card styling */
[data-testid="stVerticalBlock"] > div:has(> [data-testid="stContainer"]) {
    width: 100%;
}

/* Card container fixed dimensions */
[data-testid="stContainer"] {
    min-height: 160px;
    max-height: 200px;
}

/* Number input compact */
[data-testid="stNumberInput"] {
    max-width: 80px;
}

/* Popover button small */
.stPopover button {
    padding: 2px 8px !important;
    font-size: 12px !important;
    min-height: auto !important;
}

/* Phase header full width */
.phase-header {
    width: 100%;
}
</style>
""", unsafe_allow_html=True)
```

---

## Alternative: Custom HTML Card with Everything Inline

If Streamlit components don't align well, use pure HTML card:

```python
def render_capability_card_html(cell):
    """Pure HTML card with inline info."""
    cap_id = cell['id']
    full_desc = get_capability_full_description(cap_id)
    desc_escaped = full_desc.replace('"', '&quot;').replace("'", "&#39;")
    
    st.markdown(f'''
    <div style="
        background: white;
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 12px;
        min-height: 140px;
        max-width: 180px;
        width: 100%;
    ">
        <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
            <span style="font-weight: 600; font-size: 12px; color: #333;">
                {cell['name']}
            </span>
            <span title="{desc_escaped}" style="cursor: help; font-size: 14px;">ℹ️</span>
        </div>
        <div style="font-size: 10px; color: #888; font-style: italic; margin-bottom: 10px;">
            {cell.get('subtitle', '')}
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Streamlit inputs below (constrained width)
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("I", 0, 10, 0, key=f"i_{cap_id}", label_visibility="visible")
        with col2:
            st.number_input("R", 0, 10, 0, key=f"r_{cap_id}", label_visibility="visible")
```

---

## Summary of Changes

| Issue | Fix |
|-------|-----|
| App too wide | `max-width: 1000px` on `.block-container` |
| Cards inconsistent | Fixed columns (5 per row) with equal widths |
| Info button floating | Move inside card, use `st.popover` with small button |
| Inputs disconnected | Put inputs inside same `st.container(border=True)` |
| Input too wide | Add CSS `max-width: 80px` on number inputs |

---

## Testing

1. Desktop: App should be centered, max 1000px wide
2. All cards same width within each row
3. Info button inside card (top right or below text)
4. I/R inputs inside each card, compact
5. Mobile: Should still stack properly by phase
