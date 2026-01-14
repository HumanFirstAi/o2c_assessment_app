# CLAUDE.md - Implement LLM Synthesis

## Task

Update `modules/report_generator.py` to use Claude API for strategic synthesis 
while keeping knowledge_base.json as the ONLY source of truth.

## Read These Files First

1. `spec_claude_synthesis.md` - Main implementation spec
2. `spec_static_sections.md` - Static MCP guide content

## Summary of Changes

### What to ADD:

1. **Claude API client initialization**
   ```python
   import anthropic
   client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
   ```

2. **VALID_AGENTS constant** - List of all valid agent names

3. **SYNTHESIS_SYSTEM_PROMPT** - Constrains Claude to only use provided content

4. **synthesize_with_claude()** function - Calls Claude API with context

5. **Context formatters:**
   - `format_gap_context()` - Formats urgent gap data
   - `format_strength_context()` - Formats strength data  
   - `format_executive_context()` - Formats exec summary data

6. **Static section constants:**
   - `MCP_GUIDE_SECTION` - From spec_static_sections.md
   - `AGENT_GUIDE_SECTION` - From spec_static_sections.md

### What to KEEP:

- All priority calculation logic (pure math)
- KB lookup functions
- Priority matrix generation
- Score analysis functions

### What to REMOVE:

- "What We Expect in 2026" section (hardcoded generic text)
- "What's Available Today" aggregated list section
- Any validation warnings that are too aggressive

## Final Report Structure

```
1. Executive Summary          ← Claude synthesizes from computed data
2. Priority Matrix            ← Template/table (no LLM)
3. Urgent Gaps - Detailed     ← Claude synthesizes each gap
4. Strengths to Protect       ← Claude synthesizes each strength
5. Getting Started with Zuora MCP  ← Static text
6. Building Your First Zuora Agent ← Static text
```

## Key Principle

```
KB (facts) → Python (extract & format) → Claude (synthesize prose)
                                              ↓
                                    Claude CANNOT add new facts
                                    Claude CAN connect & contextualize
```

## Test After Implementation

```
http://localhost:8501/?test=mixed
```

Generate report and verify:
- Agent names match VALID_AGENTS list
- No speculative language
- Prose flows naturally
- Content is grounded in KB
