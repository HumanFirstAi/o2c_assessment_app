# SPEC: Claude API Synthesis Integration

## Overview

Add Claude API calls to synthesize report content strategically while using 
knowledge_base.json as the ONLY source of truth.

**Principle:** Claude is the EDITOR, not the AUTHOR. The KB is the author.

---

## 1. Update Dependencies

Add to `requirements.txt` if not present:
```
anthropic>=0.18.0
```

---

## 2. Update modules/report_generator.py

### 2.1 Add Imports and Client

```python
import anthropic
import os
import re
from typing import Optional

# Initialize client
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
```

### 2.2 Define Valid Agents Constant

```python
VALID_AGENTS = [
    "Anantha Concierge",
    "Billing Operations Agent",
    "Churn Agent",
    "Collections Manager Agent",
    "Customer Health Agent",
    "Customer Success Agent",
    "DQ/Trino Agent",
    "Data Management Agent",
    "DataFix AI",
    "Developer MCP",
    "Finance Intelligence Agent",
    "Fulfillment Agent",
    "Mediation/DACO Agent",
    "Notification AI Bot",
    "Outcomes Simulation Agent",
    "Provisioning Agent",
    "Query Assistant",
    "Quote Agent",
    "RCA Agent",
    "Reconciliation AI",
    "Revenue Accountant Agent",
    "Revenue Manager Agent",
    "Revenue Narrator",
    "Risk Scoring Agent",
    "Workflow AI Bot",
]
```

### 2.3 Create System Prompt

```python
SYNTHESIS_SYSTEM_PROMPT = """You are a strategic consultant synthesizing an 
O2C (Order-to-Cash) assessment report. You must ONLY use information provided 
in the user message - you are a librarian organizing content, not an inventor.

ABSOLUTE RULES:
1. ONLY reference agent names from the provided list
2. ONLY cite capabilities, features, and tools from the provided context
3. NO speculation - never use "could potentially", "might be able to", "consider exploring"
4. NO future tense promises or roadmap hints
5. NO invented recommendations beyond what's documented
6. Write in clear, strategic business prose
7. Be concise - quality over quantity

Your job is to CONNECT and CONTEXTUALIZE the provided facts into readable 
strategic prose. You shape and present the content, you do not create new content.

Write as if briefing a C-level executive - clear, direct, actionable."""
```

### 2.4 Create Synthesis Function

```python
def synthesize_with_claude(
    section_type: str, 
    context_content: str, 
    agents_list: list[str]
) -> str:
    """
    Use Claude to synthesize KB content into strategic prose.
    Claude can ONLY use information provided in context_content.
    
    Args:
        section_type: Type of section (executive_summary, urgent_gap, strength)
        context_content: Pre-formatted content from KB to synthesize
        agents_list: List of valid agent names Claude can reference
        
    Returns:
        Synthesized prose string
    """
    
    prompts = {
        "executive_summary": """Synthesize this into an executive summary (2-3 paragraphs).

Highlight:
- Overall readiness posture
- Most critical gaps requiring attention
- Key strengths to leverage
- The strategic opportunity with AI agents and MCP

{context}

Write for a C-level audience. Be direct and strategic.""",

        "urgent_gap": """Synthesize this urgent capability gap analysis (2-3 paragraphs).

Connect:
- Why this gap matters to their business
- What's available TODAY to address it
- Which specific agents and MCP tools are most relevant
- The business impact of closing this gap

{context}

Be specific about the agents and tools. No vague recommendations.""",

        "strength": """Synthesize this strength analysis (1-2 paragraphs).

Highlight:
- Why this capability is a competitive advantage
- How current AI agents and tools support it
- How to protect and leverage this strength

{context}

Keep it concise - strengths need less explanation than gaps.""",

        "priority_matrix": """Synthesize this priority matrix overview (1-2 paragraphs).

Explain:
- The distribution of gaps vs strengths
- Which phases need most attention
- Overall readiness pattern

{context}

Be analytical and direct."""
    }
    
    user_prompt = prompts.get(section_type, prompts["urgent_gap"]).format(
        context=context_content
    )
    
    # Add agents constraint to user prompt
    user_prompt += f"""

VALID AGENT NAMES (only reference these):
{', '.join(agents_list)}

Do NOT reference any agent not in this list."""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1500,
            system=SYNTHESIS_SYSTEM_PROMPT,
            messages=[
                {"role": "user", "content": user_prompt}
            ]
        )
        return response.content[0].text
        
    except Exception as e:
        # Fallback to template-based if API fails
        print(f"Claude API error: {e}. Falling back to template.")
        return context_content
```

### 2.5 Create Context Formatters

```python
def format_gap_context(gap: dict, kb_data: dict) -> str:
    """Format gap data for Claude synthesis."""
    
    primary = kb_data.get('agent_mapping', {}).get('primary_agents', [])
    supporting = kb_data.get('agent_mapping', {}).get('supporting_agents', [])
    platform_features = kb_data.get('current_ai_capabilities', {}).get('platform_features', [])
    mcp_tools = kb_data.get('current_ai_capabilities', {}).get('mcp_tools', [])
    
    return f"""
CAPABILITY: {gap['name']}
PHASE: {gap['phase']}
SCORES: Importance={gap['importance']}, Readiness={gap['readiness']}, Gap Score={gap.get('gap_score', 'N/A')}
PRIORITY: URGENT GAP (High Importance + Low Readiness)

WHY IT MATTERS:
{kb_data.get('why_it_matters', 'Not documented')}

WHAT'S AVAILABLE TODAY:
{kb_data.get('how_it_works_today', 'Not documented')}

PLATFORM FEATURES:
{chr(10).join('- ' + f for f in platform_features[:5]) if platform_features else '- None documented'}

PRIMARY AI AGENTS:
{chr(10).join('- ' + a for a in primary) if primary else '- None documented'}

SUPPORTING AI AGENTS:
{chr(10).join('- ' + a for a in supporting) if supporting else '- None documented'}

MCP TOOLS AVAILABLE:
{chr(10).join('- ' + t for t in mcp_tools[:5]) if mcp_tools else '- None documented'}
"""


def format_strength_context(strength: dict, kb_data: dict) -> str:
    """Format strength data for Claude synthesis."""
    
    primary = kb_data.get('agent_mapping', {}).get('primary_agents', [])
    supporting = kb_data.get('agent_mapping', {}).get('supporting_agents', [])
    
    return f"""
CAPABILITY: {strength['name']}
PHASE: {strength['phase']}
SCORES: Importance={strength['importance']}, Readiness={strength['readiness']}
PRIORITY: STRENGTH (High Importance + High Readiness)

WHY IT MATTERS:
{kb_data.get('why_it_matters', 'Not documented')}

WHAT'S WORKING TODAY:
{kb_data.get('how_it_works_today', 'Not documented')}

AI AGENTS SUPPORTING THIS:
Primary: {', '.join(primary) if primary else 'None documented'}
Supporting: {', '.join(supporting) if supporting else 'None documented'}
"""


def format_executive_context(
    company_name: str,
    total_scored: int,
    urgent_gaps: list,
    critical_gaps: list,
    strengths: list,
    avg_importance: float,
    avg_readiness: float
) -> str:
    """Format executive summary context for Claude synthesis."""
    
    return f"""
COMPANY: {company_name}
ASSESSMENT SCOPE: {total_scored} capabilities scored

OVERALL METRICS:
- Average Importance: {avg_importance:.1f}/10
- Average Readiness: {avg_readiness:.1f}/10
- Readiness Gap: {avg_importance - avg_readiness:.1f} points

PRIORITY DISTRIBUTION:
- Urgent Gaps (High I, Low R): {len(urgent_gaps)}
- Critical Gaps (High I, Medium R): {len(critical_gaps)}
- Strengths (High I, High R): {len(strengths)}

TOP 3 URGENT GAPS:
{chr(10).join(f"- {g['name']} ({g['phase']}): I={g['importance']}, R={g['readiness']}" for g in urgent_gaps[:3])}

TOP 3 STRENGTHS:
{chr(10).join(f"- {s['name']} ({s['phase']}): I={s['importance']}, R={s['readiness']}" for s in strengths[:3])}

PHASES WITH MOST GAPS:
{format_phase_gap_summary(urgent_gaps)}
"""


def format_phase_gap_summary(gaps: list) -> str:
    """Count gaps by phase."""
    phase_counts = {}
    for gap in gaps:
        phase = gap.get('phase', 'Unknown')
        phase_counts[phase] = phase_counts.get(phase, 0) + 1
    
    sorted_phases = sorted(phase_counts.items(), key=lambda x: x[1], reverse=True)
    return chr(10).join(f"- {phase}: {count} gaps" for phase, count in sorted_phases[:3])
```

### 2.6 Update Main Report Generation Function

```python
def generate_report(
    scores: dict, 
    knowledge_base: dict, 
    company_name: str = "Company",
    use_llm_synthesis: bool = True
) -> str:
    """
    Generate strategic assessment report.
    
    Args:
        scores: Dict of capability_id -> {importance, readiness}
        knowledge_base: Full KB JSON
        company_name: Company name for report header
        use_llm_synthesis: If True, use Claude for prose. If False, template only.
    
    Returns:
        Complete report as markdown string
    """
    
    # Step 1: Compute priorities (pure math - no LLM)
    analyzed = analyze_all_scores(scores, knowledge_base)
    urgent_gaps = [c for c in analyzed if c['category'] == 'URGENT_GAP']
    critical_gaps = [c for c in analyzed if c['category'] == 'CRITICAL_GAP']
    strengths = [c for c in analyzed if c['category'] == 'STRENGTH']
    
    # Calculate averages
    all_i = [s['importance'] for s in analyzed]
    all_r = [s['readiness'] for s in analyzed]
    avg_importance = sum(all_i) / len(all_i) if all_i else 0
    avg_readiness = sum(all_r) / len(all_r) if all_r else 0
    
    # Step 2: Generate sections
    if use_llm_synthesis:
        # Use Claude to synthesize prose
        
        # Executive Summary
        exec_context = format_executive_context(
            company_name, len(analyzed), urgent_gaps, critical_gaps, 
            strengths, avg_importance, avg_readiness
        )
        executive_summary = synthesize_with_claude(
            "executive_summary", exec_context, VALID_AGENTS
        )
        
        # Urgent Gaps
        urgent_sections = []
        for gap in urgent_gaps:
            kb_data = get_capability_from_kb(gap['id'], knowledge_base)
            if kb_data:
                context = format_gap_context(gap, kb_data)
                synthesis = synthesize_with_claude("urgent_gap", context, VALID_AGENTS)
                urgent_sections.append(f"### {gap['name']}\n**Phase:** {gap['phase']} | **Scores:** I={gap['importance']}, R={gap['readiness']}\n\n{synthesis}")
        
        # Strengths
        strength_sections = []
        for strength in strengths:
            kb_data = get_capability_from_kb(strength['id'], knowledge_base)
            if kb_data:
                context = format_strength_context(strength, kb_data)
                synthesis = synthesize_with_claude("strength", context, VALID_AGENTS)
                strength_sections.append(f"### {strength['name']}\n**Phase:** {strength['phase']} | **Scores:** I={strength['importance']}, R={strength['readiness']}\n\n{synthesis}")
    
    else:
        # Template-only fallback (no LLM calls)
        executive_summary = generate_template_executive_summary(...)
        urgent_sections = [generate_template_gap(g, kb) for g in urgent_gaps]
        strength_sections = [generate_template_strength(s, kb) for s in strengths]
    
    # Step 3: Assemble report
    report = f"""# O2C AI & MCP Readiness Assessment
## {company_name}
*Generated: {datetime.now().strftime('%Y-%m-%d')}*

---

## 1. Executive Summary

{executive_summary}

---

## 2. Priority Matrix

{generate_priority_matrix_table(analyzed)}

---

## 3. Urgent Gaps - Detailed Analysis

{chr(10).join(urgent_sections) if urgent_sections else "*No urgent gaps identified.*"}

---

## 4. Strengths to Protect

{chr(10).join(strength_sections) if strength_sections else "*No significant strengths identified.*"}

---

## 5. Getting Started with Zuora MCP

{MCP_GUIDE_SECTION}

---

## 6. Building Your First Zuora Agent

{AGENT_GUIDE_SECTION}
"""
    
    return report
```

---

## 3. Key Principle Diagram

```
┌─────────────────────────────────────────────────────────┐
│  KNOWLEDGE BASE (JSON) - SOURCE OF TRUTH                │
│  Contains: Agent names, capabilities, tools, features   │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│  PYTHON CODE - COMPUTATION & EXTRACTION                 │
│  1. Calculates priorities from I/R scores               │
│  2. Extracts relevant KB content for each capability    │
│  3. Formats context strings for Claude                  │
│  4. Passes ONLY KB content to Claude                    │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│  CLAUDE LLM - SYNTHESIS ONLY                            │
│  - Receives pre-extracted KB content                    │
│  - Synthesizes into strategic prose                     │
│  - CANNOT add facts not in input                        │
│  - Connects dots, frames impact, flows naturally        │
└─────────────────────────────────────────────────────────┘
```

---

## 4. Testing

Test URL with synthesis:
```
http://localhost:8501/?test=mixed
```

Generate report and verify:
1. All agent names in output exist in VALID_AGENTS
2. No speculative language ("could potentially", "might")
3. Content matches KB source data
4. Prose flows naturally and connects concepts
