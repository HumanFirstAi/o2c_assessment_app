# CLAUDE.md - Empty Start Values & Zero Handling

## Task

Update input fields to start empty and handle zero values gracefully.

---

## 1. Change Input Fields to Start Empty

**In modules/interactive_form.py:**

**CHANGE FROM:**
```python
i_val = st.number_input("I", 1, 10, 5, key=f"i_{cap_id}")
r_val = st.number_input("R", 1, 10, 5, key=f"r_{cap_id}")
```

**CHANGE TO:**
```python
i_val = st.number_input(
    "I", 
    min_value=0, 
    max_value=10, 
    value=0,  # Start empty (0 means not filled)
    key=f"i_{cap_id}",
    label_visibility="collapsed"
)
r_val = st.number_input(
    "R", 
    min_value=0, 
    max_value=10, 
    value=0,  # Start empty (0 means not filled)
    key=f"r_{cap_id}",
    label_visibility="collapsed"
)
```

---

## 2. Update Progress Counter

Only count capabilities where BOTH I and R are > 0:

**CHANGE FROM:**
```python
scored_count = sum(1 for cap in capabilities if 
    st.session_state.get(f"i_{cap['id']}", 0) > 0)
```

**CHANGE TO:**
```python
def count_completed_capabilities() -> int:
    """Count capabilities where both I and R are filled (> 0)."""
    from grid_layout import get_all_capabilities
    count = 0
    for cap in get_all_capabilities():
        i_val = st.session_state.get(f"i_{cap['id']}", 0)
        r_val = st.session_state.get(f"r_{cap['id']}", 0)
        if i_val > 0 and r_val > 0:
            count += 1
    return count

# In sidebar
scored = count_completed_capabilities()
total = 38  # TOTAL_CAPABILITIES
st.progress(scored / total)
st.caption(f"{scored}/{total} capabilities scored")
```

---

## 3. Add Confirmation Dialog on Generate

**In app.py, update the Generate Report button:**

```python
def get_zero_capabilities() -> list:
    """Get list of capabilities with 0 in either I or R."""
    from grid_layout import get_all_capabilities
    zeros = []
    for cap in get_all_capabilities():
        i_val = st.session_state.get(f"i_{cap['id']}", 0)
        r_val = st.session_state.get(f"r_{cap['id']}", 0)
        if i_val == 0 or r_val == 0:
            zeros.append(cap['name'])
    return zeros


def collect_valid_scores() -> dict:
    """Collect only scores where both I and R are > 0."""
    from grid_layout import get_all_capabilities
    scores = {}
    for cap in get_all_capabilities():
        i_val = st.session_state.get(f"i_{cap['id']}", 0)
        r_val = st.session_state.get(f"r_{cap['id']}", 0)
        # Only include if BOTH are filled
        if i_val > 0 and r_val > 0:
            scores[cap['id']] = {
                'name': cap['name'],
                'phase': cap.get('phase_id', ''),
                'importance': i_val,
                'readiness': r_val
            }
    return scores


# Generate Report button with confirmation
if st.button("📊 Generate Report", type="primary", use_container_width=True):
    zero_caps = get_zero_capabilities()
    
    if zero_caps:
        st.session_state['show_zero_warning'] = True
        st.session_state['zero_count'] = len(zero_caps)
    else:
        st.session_state['confirm_generate'] = True

# Show warning dialog if there are zeros
if st.session_state.get('show_zero_warning', False):
    st.warning(f"⚠️ You have left some values as 0. {st.session_state['zero_count']} capabilities with 0 in either Importance or Readiness will be ignored and not assessed.")
    
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
    
    with st.spinner("Generating report..."):
        scores = collect_valid_scores()
        
        if len(scores) == 0:
            st.error("No capabilities scored. Please fill in at least one capability with both I and R values.")
        else:
            report = generate_report(scores, knowledge_base, company_name)
            st.session_state['generated_report'] = report
            st.rerun()
```

---

## 4. Alternative: Use Modal Dialog

For a cleaner popup effect, use st.dialog (Streamlit 1.33+):

```python
@st.dialog("Confirm Generation")
def confirm_zero_dialog(zero_count: int):
    st.warning(f"⚠️ You have left some values as 0.")
    st.markdown(f"**{zero_count} capabilities** with 0 in either Importance or Readiness will be ignored and not assessed.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Cancel", use_container_width=True):
            st.rerun()
    with col2:
        if st.button("Continue", type="primary", use_container_width=True):
            st.session_state['do_generate'] = True
            st.rerun()


# In main flow
if st.button("📊 Generate Report", type="primary"):
    zero_caps = get_zero_capabilities()
    if zero_caps:
        confirm_zero_dialog(len(zero_caps))
    else:
        st.session_state['do_generate'] = True

if st.session_state.get('do_generate', False):
    st.session_state['do_generate'] = False
    scores = collect_valid_scores()
    # ... generate report
```

---

## 5. Update Score Analyzer to Filter Zeros

**In modules/score_analyzer.py:**

```python
def analyze_all_scores(scores: dict, knowledge_base: dict) -> list:
    """Analyze scores - only processes non-zero entries."""
    analyzed = []
    
    for cap_id, score_data in scores.items():
        importance = score_data.get('importance', 0)
        readiness = score_data.get('readiness', 0)
        
        # Skip if either is 0
        if importance == 0 or readiness == 0:
            continue
        
        # ... rest of analysis
```

---

## Summary

| Change | Before | After |
|--------|--------|-------|
| Starting value | 5 | 0 (empty) |
| Min value | 1 | 0 |
| Zero handling | N/A | Ignored in report |
| Generate click | Direct | Confirmation if zeros exist |
| Progress count | Any value | Only both I and R > 0 |

---

## Dialog Message

```
⚠️ You have left some values as 0. 
X capabilities with 0 in either Importance or Readiness will be ignored and not assessed.

[Cancel]  [Continue]
```
