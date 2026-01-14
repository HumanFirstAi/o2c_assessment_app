# O2C AI Agent & MCP Readiness Assessment App

## Project Overview
Build a Streamlit application with TWO input methods:
1. **Interactive digital form** - Online version matching the HTML template exactly
2. **Image upload** - Extract scores from completed paper assessments using Claude Vision

Both methods generate a strategic priority guide for AI Agent and MCP adoption.

## Key Files - READ IN THIS ORDER
1. `CLAUDE.md` - This file (quick reference)
2. `o2c_assessment_app_spec.md` - Core specification 
3. `spec_addendum_interactive.md` - Interactive form & grid layout details
4. `grid_layout.py` - Exact 8×7 grid cell mappings (42 capabilities + 14 empty)
5. `knowledge_base.json` - Complete AI/MCP context for all capabilities
6. `lifecycle_assessment.html` - Reference HTML template (match this exactly!)

## Build Instructions

### 1. Project Structure
```
o2c_assessment_app/
├── app.py                      # Main Streamlit app with 2 tabs
├── requirements.txt            # Dependencies
├── config.py                   # Configuration
├── knowledge_base.json         # Capability knowledge base
├── grid_layout.py              # Grid cell mappings
├── modules/
│   ├── __init__.py
│   ├── interactive_form.py     # Tab 1: Interactive assessment grid
│   ├── image_processor.py      # Tab 2: Claude Vision extraction
│   ├── score_analyzer.py       # Priority analysis engine
│   ├── report_generator.py     # LLM report generation
│   └── export_handler.py       # DOCX/PDF/JSON export
└── templates/
    ├── lifecycle_assessment.html  # Reference template
    └── styles.css
```

### 2. Build Order
1. Copy `grid_layout.py` (provided - defines exact grid structure)
2. Copy `knowledge_base.json` (provided - complete AI/MCP context)
3. Create `config.py` from main spec Section 10
4. Create `modules/interactive_form.py` - see spec_addendum_interactive.md
5. Create `modules/image_processor.py` from main spec Section 5
6. Create `modules/score_analyzer.py` from main spec Section 6
7. Create `modules/report_generator.py` from main spec Section 7
8. Create `modules/export_handler.py` for DOCX/PDF/JSON export
9. Create `app.py` with TWO TABS (see below)
10. Create `requirements.txt` from main spec Section 8.3

### 3. TWO INPUT MODES (Critical!)

**Tab 1: "📝 Interactive Assessment"**
- Render 8×7 grid EXACTLY matching lifecycle_assessment.html
- Use grid_layout.py for cell positions and phase colors
- Each capability card shows:
  - Name (bold)
  - Subtitle (italic gray, if present)
  - Two side-by-side number inputs: I (pink bg) and R (teal bg)
- Empty cells (None in grid_layout.py) show as grayed "—"
- Real-time priority color on card border as user enters scores
- Hover tooltip showing AI context from knowledge_base.json
- Progress bar in sidebar
- Save/Load JSON buttons

**Tab 2: "📤 Upload Completed Form"**
- File uploader for PNG/JPG/PDF
- Use Claude Vision to extract I/R scores
- Show extracted scores for verification
- Allow editing before analysis

**Both tabs → same report generation**

### 4. Visual Design (Must Match HTML Template!)

- Phase header colors from grid_layout.py PHASES
- Importance (I): bg #fce4ec, border dashed #E6007E
- Readiness (R): bg #e0f7fa, border dashed #00A5A8
- Empty cells: bg #fafafa, border #eee
- Capability cards: white bg, #ddd border
- Feedback loop pill at bottom with gradient #1976D2 → #2E7D32

### 5. Core Functionality

**Interactive Form (modules/interactive_form.py)**
- Render grid from grid_layout.py
- st.number_input for each I/R score (1-10)
- Skip None cells (empty)
- Store scores in st.session_state
- See spec_addendum_interactive.md Section 2 for code examples

**Image Processing (modules/image_processor.py)**
- Use Anthropic Claude Vision API to extract I/R scores from uploaded assessment images
- Return structured JSON with capability name, importance (1-10), readiness (1-10)
- Handle validation and warnings for unclear extractions
- Use extraction prompt from spec_addendum_interactive.md Section 4

**Score Analyzer (modules/score_analyzer.py)**
- Categorize each capability: URGENT_GAP, CRITICAL_GAP, STRENGTH, OPPORTUNITY, MAINTAIN, DEPRIORITIZE
- Calculate gap scores: `importance * (10 - readiness) / 10`
- Map to timeline: NOW (0-6M), NEAR (6-12M), LATER (12-24M)

**Report Generator (modules/report_generator.py)**
- Use Claude API to generate strategic report
- Include: Executive Summary, Priority Matrix, Urgent Gaps Detail, Agent Roadmap, MCP Integration Plan
- Reference specific agents and MCP tools from knowledge base

**Export Handler (modules/export_handler.py)**
- Export to DOCX using python-docx
- Export to PDF using weasyprint or similar
- Export to Markdown
- Export to JSON (for save/load)

### 6. Key Dependencies
```
streamlit>=1.30.0
anthropic>=0.18.0
python-docx>=1.1.0
Pillow>=10.0.0
pandas>=2.0.0
plotly>=5.18.0
pydantic>=2.0.0
python-dotenv>=1.0.0
```

### 7. Environment Variables
```
ANTHROPIC_API_KEY=<required>
```

## Important Notes

- **42 capabilities** need I/R scores (see grid_layout.py)
- **14 empty cells** shown as "—" (no input)
- Use Claude Vision (claude-sonnet-4-20250514) for image score extraction
- The report should reference actual agent names: "Billing Operations Agent", "Revenue Narrator", "Churn Agent", etc.
- Priority matrix logic: High I (≥7) + Low R (≤4) = URGENT_GAP
- Interactive form must visually match lifecycle_assessment.html exactly

## Grid Layout Quick Reference

| Phase | Color | Capabilities |
|-------|-------|--------------|
| Configure & Price | #2E7D32 (green) | 5 |
| Quote & Sell | #1565C0 (blue) | 6 |
| Invoice | #7B1FA2 (purple) | 6 |
| Collect | #00838F (teal) | 5 |
| Provision | #F9A825 (yellow) | 4 |
| Recognize & Report | #6A1B9A (dark purple) | 6 |
| Learn | #EF6C00 (orange) | 7 |
| Sustain & Grow | #1976D2 (blue) | 3 |

## Testing
Run locally with: `streamlit run app.py`

## Reference Files
- Full specification: `o2c_assessment_app_spec.md`
- Interactive form spec: `spec_addendum_interactive.md`
- Grid structure: `grid_layout.py`
- AI/MCP context: `knowledge_base.json`
- Visual reference: `lifecycle_assessment.html`
