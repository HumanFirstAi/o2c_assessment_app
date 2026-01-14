# CLAUDE.md - UI Style Updates

## Task

Make these 3 UI changes.

---

## 1. Report Max-Width

Update report display styling so paragraphs have max-width of 600px.

**In app.py or where report is displayed:**

```python
# Wrap report display with max-width container
st.markdown("""
<style>
.report-container {
    max-width: 600px;
}
.report-container p {
    max-width: 600px;
}
</style>
""", unsafe_allow_html=True)

# Display report in container
st.markdown(f'<div class="report-container">{report}</div>', unsafe_allow_html=True)
```

**Or add global style at top of app.py:**

```python
st.markdown("""
<style>
/* Report paragraphs max width */
.stMarkdown p {
    max-width: 600px;
}
</style>
""", unsafe_allow_html=True)
```

---

## 2. Increase Font Sizes in Capability Cards

**In modules/interactive_form.py:**

Update the card HTML styling:

**CHANGE FROM:**
```python
font-size: 11px;   # capability name
font-size: 9px;    # subtitle
```

**CHANGE TO:**
```python
font-size: 15px;   # capability name
font-size: 12px;   # subtitle
```

**Full card HTML update:**

```python
card_html = f'''
<div style="
    background: white; 
    border: 2px solid {border_color}; 
    border-radius: 4px; 
    padding: 10px; 
    height: 100px;
    min-height: 100px;
    max-height: 100px;
    overflow: hidden;
">
    <div style="
        font-weight: 600; 
        font-size: 15px; 
        color: #333; 
        line-height: 1.2;
        margin-bottom: 4px;
    ">
        {cell['name']}
    </div>
    <div style="
        font-size: 12px; 
        color: #888; 
        font-style: italic;
        line-height: 1.3;
    ">
        {cell.get('subtitle', '')}
    </div>
</div>
'''
```

---

## 3. Update Instructions Text

**Find this text in app.py or modules/interactive_form.py:**

```python
"Fill out the assessment directly in the grid below..."
```

**CHANGE TO:**

```python
"Each capability card allows you to enter I (Importance) and R (Readiness) scores from 1-10."
```

**Or if it's in st.markdown:**

```python
st.markdown("Each capability card allows you to enter **I** (Importance) and **R** (Readiness) scores from 1-10.")
```

---

## Summary

| Change | Location | Before | After |
|--------|----------|--------|-------|
| Report width | app.py | unlimited | max-width: 600px |
| Card title font | interactive_form.py | 11px | 15px |
| Card subtitle font | interactive_form.py | 9px | 12px |
| Instructions | app.py | old text | "Each capability card allows you to enter I (Importance) and R (Readiness) scores from 1-10." |
