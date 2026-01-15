import anthropic
import json
import os
import re
import time
from typing import Dict, List
from datetime import datetime
import config
from modules.score_analyzer import (
    analyze_capabilities,
    create_priority_matrix,
    get_capabilities_by_category,
    get_phase_summary
)

# Simple rate limiter to prevent API overload
_last_api_call = 0
_api_call_interval = 0.5  # Minimum 0.5 seconds between calls (120 calls/min max)

# Initialize Claude API client
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def sanitize_branding(text: str) -> str:
    """Remove Zuora branding except for MCP-related references."""

    # Preserve these exact phrases (MCP-related)
    preserved_phrases = {
        "Zuora MCP": "PLACEHOLDER_MCP_1",
        "Zuora Developer MCP": "PLACEHOLDER_MCP_2",
        "zuora-mcp": "PLACEHOLDER_MCP_3",
        "Zuora OAuth": "PLACEHOLDER_MCP_4",
        "Zuora tenant": "PLACEHOLDER_MCP_5",
        "Zuora REST": "PLACEHOLDER_MCP_6",
        "Zuora SDK": "PLACEHOLDER_MCP_7",
    }

    # Temporarily replace preserved phrases
    for phrase, placeholder in preserved_phrases.items():
        text = text.replace(phrase, placeholder)

    # Remove remaining Zuora mentions
    text = re.sub(r'\bZuora\s+', '', text)  # "Zuora " -> ""
    text = re.sub(r'\bZuora\'s\s+', '', text)  # "Zuora's " -> ""
    text = re.sub(r'\bZuora\b', '', text)  # standalone "Zuora" -> ""

    # Restore preserved phrases
    for phrase, placeholder in preserved_phrases.items():
        text = text.replace(placeholder, phrase)

    # Clean up any double spaces
    text = re.sub(r'  +', ' ', text)

    return text


def fix_bullet_formatting(text: str) -> str:
    """
    Force bullets onto separate lines.
    Handles: "Text: • Item 1 • Item 2" -> "Text:\n• Item 1\n• Item 2"
    Preserves text before the first bullet.
    """
    # First, normalize any weird bullet characters
    text = text.replace('●', '•').replace('○', '•')

    # Check if there are any bullets
    if '•' not in text:
        return text

    # Find the position of the first bullet
    first_bullet_idx = text.find('•')

    # Split into prefix (before first bullet) and bullet content
    prefix = text[:first_bullet_idx].strip()
    bullet_content = text[first_bullet_idx:]

    # Split on bullets
    parts = re.split(r'\s*•\s*', bullet_content)

    # Filter empty parts and strip whitespace
    parts = [p.strip() for p in parts if p.strip()]

    # Rejoin with newlines and bullets
    if parts:
        formatted_bullets = '\n• '.join(parts)
        if prefix:
            # Keep prefix separate, add newline before bullets
            return f"{prefix}\n• {formatted_bullets}"
        else:
            return f"• {formatted_bullets}"

    return text


def fix_all_bullet_sections(report: str) -> str:
    """Fix bullet formatting in all sections of the report."""

    # Find sections that have bullets
    sections = [
        "Platform Features:",
        "MCP Tools:",
        "What's Coming:",
        "AI Agents:",
        "Available Today:",
    ]

    for section in sections:
        # Find content after section header until next section or double newline
        pattern = rf'(\*\*{re.escape(section)}\*\*\s*)(.*?)(?=\n\n|\*\*[A-Z]|\Z)'

        def fix_match(match):
            header = match.group(1)
            content = match.group(2)
            fixed_content = fix_bullet_formatting(content)
            return header + '\n' + fixed_content

        report = re.sub(pattern, fix_match, report, flags=re.DOTALL)

    return report


# System prompt for Claude synthesis
SYNTHESIS_SYSTEM_PROMPT = """You are a strategic consultant synthesizing an O2C (Order-to-Cash) assessment report. You must ONLY use information provided in the user message - you are a librarian organizing content, not an inventor.

ABSOLUTE RULES:
1. ONLY reference agent names from the provided list
2. ONLY cite capabilities, features, and tools from the provided context
3. NO speculation - never use "could potentially", "might be able to", "consider exploring"
4. NO future tense promises or roadmap hints
5. NO invented recommendations beyond what's documented
6. Write in clear, strategic business prose
7. Be concise - quality over quantity

Your job is to CONNECT and CONTEXTUALIZE the provided facts into readable strategic prose. You shape and present the content, you do not create new content.

Write as if briefing a C-level executive - clear, direct, actionable."""


def synthesize_with_claude(
    section_type: str,
    context_content: str,
    agents_list: List[str]
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
- Overall readiness posture and key metrics
- Most critical gaps requiring immediate attention
- Which O2C phases need the most work
- The strategic opportunity with AI agents and MCP to close these gaps

{context}

Write for a C-level audience. Be direct and strategic. Focus on gap identification and readiness improvement.""",

        "urgent_gap": """Synthesize this capability gap into a STRUCTURED format.

INPUT:
{context}

OUTPUT FORMAT (follow exactly):

**Why This Matters:**
[2-3 sentences on the business problem - be specific, not generic]

**Available Today:**

*AI Agents:*
• [Agent Name] - [what it does in 5-8 words]
• [Agent Name] - [what it does in 5-8 words]

*Platform Features:*
• [Feature 1]
• [Feature 2]
• [Feature 3]

*MCP Tools:*
• [Tool 1]
• [Tool 2]

**What's Coming:**
• [Upcoming capability 1]
• [Upcoming capability 2]

**Business Impact:**
[One sentence on the outcome of closing this gap]

CRITICAL FORMATTING RULES - READ CAREFULLY:
1. Each bullet point MUST be on its own line with a line break before it
2. Use the bullet character • at the start of each line
3. NEVER EVER put multiple bullets on the same line (NO: "• Item 1 • Item 2")
4. Correct format example:
   **What's Coming:**
   • First item
   • Second item
   • Third item
5. Keep "Why This Matters" to 2-3 sentences MAX
6. Agent descriptions: "[Agent Name] - [what it does in 5-8 words]"
7. Only include the MOST relevant items, not everything
8. Be specific, not generic
9. Do NOT include timelines in "What's Coming" - just list the capabilities
""",

        "strength": """Synthesize this strength into a STRUCTURED format.

INPUT:
{context}

OUTPUT FORMAT:

**Why This Is A Strength:**
[1-2 sentences on why this capability matters]

**What's Working:**
- [Bullet key agents/features supporting this]
- [Bullet key agents/features supporting this]

**Protect By:**
[One sentence on how to maintain this advantage]

Keep it concise - strengths need less detail than gaps."""
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
        # Rate limiting: enforce minimum interval between API calls
        global _last_api_call
        current_time = time.time()
        time_since_last_call = current_time - _last_api_call

        if time_since_last_call < _api_call_interval:
            sleep_time = _api_call_interval - time_since_last_call
            time.sleep(sleep_time)

        # Make API call
        _last_api_call = time.time()
        response = client.messages.create(
            model=config.CLAUDE_MODEL,
            max_tokens=config.CLAUDE_MAX_TOKENS,
            system=SYNTHESIS_SYSTEM_PROMPT,
            messages=[
                {"role": "user", "content": user_prompt}
            ]
        )
        return response.content[0].text

    except anthropic.RateLimitError as e:
        # Handle rate limit errors with exponential backoff
        print(f"Rate limit hit: {e}. Retrying after delay...")
        time.sleep(2)  # Wait 2 seconds and retry once
        try:
            response = client.messages.create(
                model=config.CLAUDE_MODEL,
                max_tokens=config.CLAUDE_MAX_TOKENS,
                system=SYNTHESIS_SYSTEM_PROMPT,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )
            return response.content[0].text
        except Exception as retry_error:
            print(f"Retry failed: {retry_error}. Falling back to template.")
            return context_content

    except Exception as e:
        # Fallback to template-based if API fails
        print(f"Claude API error: {e}. Falling back to template.")
        return context_content


def format_gap_context(gap: Dict, kb_data: dict) -> str:
    """Format gap data for Claude synthesis."""

    primary = kb_data.get('agent_mapping', {}).get('primary_agents', [])
    supporting = kb_data.get('agent_mapping', {}).get('supporting_agents', [])
    platform_features = kb_data.get('current_ai_capabilities', {}).get('platform_features', [])
    mcp_tools = kb_data.get('current_ai_capabilities', {}).get('mcp_tools', [])

    whats_coming = kb_data.get('whats_coming', {})
    coming_capabilities = whats_coming.get('capabilities', [])

    return f"""
CAPABILITY: {gap.get('capability_name', 'Unknown')}
PHASE: {gap.get('phase_name', 'Unknown')}
SCORES: Importance={gap.get('importance', 'N/A')}, Readiness={gap.get('readiness', 'N/A')}, Gap Score={gap.get('gap_score', 'N/A')}
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

WHAT'S COMING:
{chr(10).join('- ' + c for c in coming_capabilities[:5]) if coming_capabilities else '- Not documented'}
"""


def format_strength_context(strength: Dict, kb_data: dict) -> str:
    """Format strength data for Claude synthesis."""

    primary = kb_data.get('agent_mapping', {}).get('primary_agents', [])
    supporting = kb_data.get('agent_mapping', {}).get('supporting_agents', [])

    return f"""
CAPABILITY: {strength.get('capability_name', 'Unknown')}
PHASE: {strength.get('phase_name', 'Unknown')}
SCORES: Importance={strength.get('importance', 'N/A')}, Readiness={strength.get('readiness', 'N/A')}
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
    user_name: str,
    total_scored: int,
    urgent_gaps: List[Dict],
    critical_gaps: List[Dict],
    avg_importance: float,
    avg_readiness: float
) -> str:
    """Format executive summary context for Claude synthesis.
    Focus on gap identification and overall readiness posture."""

    phase_gap_summary = format_phase_gap_summary(urgent_gaps)

    return f"""
ASSESSMENT FOR: {user_name}
ASSESSMENT SCOPE: {total_scored} capabilities scored (filtered for relevance)

OVERALL METRICS:
- Average Importance: {avg_importance:.1f}/10
- Average Readiness: {avg_readiness:.1f}/10
- Readiness Gap: {avg_importance - avg_readiness:.1f} points

PRIORITY DISTRIBUTION:
- Urgent Gaps (High I, Low R): {len(urgent_gaps)}
- Critical Gaps (High I, Medium R): {len(critical_gaps)}

TOP 5 URGENT GAPS:
{chr(10).join(f"- {g.get('capability_name', 'Unknown')} ({g.get('phase_name', 'Unknown')}): I={g.get('importance', 'N/A')}, R={g.get('readiness', 'N/A')}" for g in urgent_gaps[:5])}

PHASES WITH MOST GAPS:
{phase_gap_summary}

FOCUS: This assessment identifies capability gaps requiring immediate attention. AI agents and MCP tools provide the foundation for addressing these gaps.
"""


def format_phase_gap_summary(gaps: List[Dict]) -> str:
    """Count gaps by phase."""
    phase_counts = {}
    for gap in gaps:
        phase = gap.get('phase_name', 'Unknown')
        phase_counts[phase] = phase_counts.get(phase, 0) + 1

    sorted_phases = sorted(phase_counts.items(), key=lambda x: x[1], reverse=True)
    return chr(10).join(f"- {phase}: {count} gaps" for phase, count in sorted_phases[:3])

# Valid agent names - LLM can ONLY reference these exact names
VALID_AGENTS = [
    # Concierge
    "Anantha Concierge",
    "Zuora AI Concierge",

    # Business Agents
    "Billing Operations Agent",
    "Collections Manager Agent",
    "Revenue Accountant Agent",
    "Revenue Manager Agent",
    "Customer Success Agent",
    "Customer Health Agent",
    "Churn Agent",
    "Quote Agent",
    "Deal Assist",

    # Functional Agents
    "Billing/Invoice Service Agent",
    "Mediation/DACO Agent",
    "DQ/Trino Agent",
    "Data Management Agent",
    "RCA Agent",
    "Notification AI Bot",
    "Workflow AI Bot",

    # Specialized Agents
    "Outcomes Simulation Agent",
    "Revenue Narrator",
    "SSP Analyzer",
    "Query Assistant",
    "Reconciliation AI",
    "DataFix AI",

    # Other referenced
    "Developer MCP",
    "Provisioning Agent",
    "Fulfillment Agent",
    "Risk Scoring Agent",
    "Finance Intelligence Agent",
]

# Static MCP guide content (Sections 5-6)
MCP_GUIDE_SECTION = """
### What MCP Gives You

MCP (Model Context Protocol) is a standard way for AI tools (Claude Desktop, Cursor, ChatGPT Codex, etc.) to plug into external systems – think of it as USB for AI.

The Developer MCP Server lets AI tools:
- Query your tenant (accounts, subscriptions, invoices, etc.)
- Generate SDK code in Java, Python, Node.js, C#, curl
- Ask product questions ("How do I implement usage-based billing?")
- Help with SDK upgrades
- Create catalog & subscriptions (with approval controls)

You run this MCP server on your own machine; your AI client connects securely using your OAuth client credentials.

### Prerequisites

- A tenant (ideally sandbox/test for first setup)
- OAuth client credentials (BASE_URL, CLIENT_ID, CLIENT_SECRET)
- Node.js and npm installed

### Installation

```bash
node --version   # confirm Node is installed
npm install -g zuora-mcp
```

### Configuration for Claude Desktop

1. Open Claude Desktop: Settings → Developer tab
2. Click Edit Config to open claude_desktop_config.json
3. Add:

```json
{
  "mcpServers": {
    "zuora-developer-mcp": {
      "command": "npx",
      "args": ["-y", "zuora-mcp"],
      "env": {
        "BASE_URL": "https://rest.apisandbox.zuora.com",
        "ZUORA_CLIENT_ID": "your-client-id",
        "ZUORA_CLIENT_SECRET": "your-client-secret"
      }
    }
  }
}
```

4. Restart Claude Desktop completely

### Configuration for Cursor

1. Settings → Cursor Settings → Tools & MCP → "New MCP Server"
2. Use the same JSON configuration
3. Restart Cursor

### Available MCP Tools

| Tool | Purpose |
|------|---------|
| **zuora_codegen** | Generate SDK code (Java, Python, Node.js, C#, curl) |
| **ask_zuora** | Product knowledge Q&A |
| **sdk_upgrade** | Plan and execute SDK upgrades |
| **query_objects** | Query 40+ object types with filters |
| **create_product** | Create products (with approval) |
| **create_subscription** | Create subscriptions via Order API |

### Quick Test

Run a safe, read-only query:
```
"list all the euro billing accounts"
```

### Troubleshooting

| Issue | Solution |
|-------|----------|
| Command not found: npx | Node/npm not installed or PATH issue |
| Authentication failed | Check BASE_URL, CLIENT_ID, CLIENT_SECRET |
| Cannot find module | Run: npm install -g zuora-mcp |
"""

AGENT_GUIDE_SECTION = """
### Option 1: Use Existing Tools as Agents

Once MCP is configured, Claude Desktop or Cursor become AI-aware agents:

**Code Generation:**
```
"Generate Java SDK code to create a subscription with annual billing
and a usage add-on, using best practices."
```

**Data Queries:**
```
"List all active subscriptions for account A-0000123 created in the last 90 days."
```

**SDK Upgrades:**
```
"Help me upgrade from Java SDK v3.5.0 to v3.6.0 - what changed?"
```

### Option 2: Build Custom Agents

To embed an AI-aware agent in your own applications:

**Step 1: Define the agent's job**
- "Billing Account Explainer" – explains balance changes
- "Catalog Assistant" – proposes and creates products with approval
- "Integration Helper" – generates SDK code for specific use cases

**Step 2: Wire to MCP**
- Start: `npx -y zuora-mcp`
- Pass: BASE_URL, CLIENT_ID, CLIENT_SECRET

**Step 3: Enforce safety**
- Default to read-only queries
- Keep approval policies enabled for writes
- Log key actions

### Best Practices

| Practice | Description |
|----------|-------------|
| Start in sandbox | Use sandbox for write operations |
| Keep approval enabled | Treat MCP like privileged integration |
| Audit key actions | Log products, subscriptions, modifications |
| Secure credentials | Protect CLIENT_ID and CLIENT_SECRET |

### Getting Access

The Developer MCP server is in beta. Contact your Customer Success Manager for:
- Access to the MCP Server beta
- Latest setup guide
- Enablement resources
"""


def filter_by_importance_threshold(analyzed_scores: List[Dict]) -> List[Dict]:
    """Remove capabilities with importance 25%+ below average."""

    # Calculate average importance
    all_importance = [s['importance'] for s in analyzed_scores]
    avg_importance = sum(all_importance) / len(all_importance) if all_importance else 5

    # Threshold is 25% below average
    threshold = avg_importance * 0.75

    # Filter out low-importance items
    filtered = [s for s in analyzed_scores if s['importance'] >= threshold]

    # Log what was filtered (for debugging)
    removed = [s for s in analyzed_scores if s['importance'] < threshold]
    if removed:
        print(f"Filtered {len(removed)} capabilities below importance threshold ({threshold:.1f})")

    return filtered


def generate_strategic_report(
    scores: List[Dict],
    knowledge_base: dict,
    customer_context: dict = None
) -> str:
    """
    Generate comprehensive strategic report.
    NEW: Constrained to factual KB content only. LLM is a librarian, not an inventor.
    """

    # Prepare analysis data
    analyzed_capabilities = analyze_capabilities(scores, knowledge_base)

    # Filter out low-importance capabilities (25% below average)
    analyzed_capabilities = filter_by_importance_threshold(analyzed_capabilities)

    priority_matrix = create_priority_matrix(analyzed_capabilities)
    urgent_gaps = get_capabilities_by_category(analyzed_capabilities, "URGENT_GAP")
    critical_gaps = get_capabilities_by_category(analyzed_capabilities, "CRITICAL_GAP")
    phase_summary = get_phase_summary(analyzed_capabilities)

    # Build report with template-based sections
    report = "# O2C AI Agent & MCP Readiness Assessment\n\n"

    # Add customer context if provided
    if customer_context:
        user = customer_context.get('user', '')
        email = customer_context.get('email', '')

        if user or email:
            report += "## Assessment Context\n\n"
            if user:
                report += f"**Prepared for:** {user}\n\n"
            if email:
                report += f"**Email:** {email}\n\n"
            report += "---\n\n"

    # Section 1: Executive Summary (Claude synthesis)
    user_name = customer_context.get('user', 'User') if customer_context else 'User'
    report += generate_executive_summary(analyzed_capabilities, priority_matrix, urgent_gaps, critical_gaps, user_name)

    # Section 2: Priority Matrix Analysis (Template-based)
    report += generate_priority_matrix_section(priority_matrix, phase_summary)

    # Section 3: Urgent Gaps - Detailed Analysis (Template-based from KB)
    report += generate_urgent_gaps_section(urgent_gaps, knowledge_base)

    # Section 4: Getting Started with Zuora MCP (STATIC)
    report += "## 4. Getting Started with Zuora MCP\n\n" + MCP_GUIDE_SECTION + "\n\n"

    # Section 5: Building Your First Zuora Agent (STATIC)
    report += "## 5. Building Your First Zuora Agent\n\n" + AGENT_GUIDE_SECTION + "\n\n"

    # Validate report
    warnings = validate_report(report)
    if warnings:
        report += "\n\n---\n\n## Report Validation Warnings\n\n"
        for warning in warnings:
            report += f"- {warning}\n"

    # Fix bullet formatting (ensure bullets on separate lines)
    report = fix_all_bullet_sections(report)

    # Sanitize branding (remove Zuora except MCP references)
    report = sanitize_branding(report)

    return report


def generate_executive_summary(analyzed_capabilities: List[Dict], priority_matrix: Dict,
                               urgent_gaps: List[Dict], critical_gaps: List[Dict],
                               user_name: str = "User") -> str:
    """
    Generate executive summary using Claude synthesis.
    Focus on gap identification and overall readiness posture.
    """
    # Calculate facts
    total_caps = len(analyzed_capabilities)

    avg_importance = sum(c['importance'] for c in analyzed_capabilities) / total_caps if total_caps > 0 else 0
    avg_readiness = sum(c['readiness'] for c in analyzed_capabilities) / total_caps if total_caps > 0 else 0

    # Format context for Claude
    exec_context = format_executive_context(
        user_name, total_caps, urgent_gaps, critical_gaps,
        avg_importance, avg_readiness
    )

    # Synthesize with Claude
    synthesis = synthesize_with_claude("executive_summary", exec_context, VALID_AGENTS)

    summary = "## 1. Executive Summary\n\n"
    summary += synthesis + "\n\n"
    summary += "---\n\n"
    return summary


def generate_priority_matrix_section(priority_matrix: Dict, phase_summary: Dict) -> str:
    """Generate priority matrix analysis section."""
    section = "## 2. Priority Matrix Analysis\n\n"

    section += "### Distribution by Priority Category\n\n"
    section += "| Category | Count | Description |\n"
    section += "|----------|-------|-------------|\n"
    section += f"| Urgent Gap | {priority_matrix.get('URGENT_GAP', 0)} | High importance (≥7), Low readiness (≤4) |\n"
    section += f"| Critical Gap | {priority_matrix.get('CRITICAL_GAP', 0)} | High importance (≥7), Medium readiness (5-6) |\n"
    section += f"| Strength | {priority_matrix.get('STRENGTH', 0)} | High importance (≥7), High readiness (≥7) |\n"
    section += f"| Opportunity | {priority_matrix.get('OPPORTUNITY', 0)} | Medium importance (4-6), Low readiness (≤4) |\n"
    section += f"| Maintain | {priority_matrix.get('MAINTAIN', 0)} | Medium importance (4-6), High readiness (≥7) |\n"
    section += f"| Deprioritize | {priority_matrix.get('DEPRIORITIZE', 0)} | Low importance (≤3) |\n\n"

    section += "### Phase-Level Summary\n\n"
    section += "| Phase | Avg Importance | Avg Readiness | Avg Gap Score | Urgent Gaps | Strengths |\n"
    section += "|-------|----------------|---------------|---------------|-------------|----------|\n"

    for phase_id, data in phase_summary.items():
        section += f"| {data['phase_name']} | {data['avg_importance']:.1f} | {data['avg_readiness']:.1f} | "
        section += f"{data['avg_gap_score']:.1f} | {data['urgent_count']} | {data['strength_count']} |\n"

    section += "\n---\n\n"
    return section


def generate_urgent_gaps_section(urgent_gaps: List[Dict], knowledge_base: dict) -> str:
    """
    Generate urgent gaps section using Claude synthesis.
    """
    if not urgent_gaps:
        return "## 3. Urgent Gaps - Detailed Analysis\n\nNo urgent gaps identified.\n\n---\n\n"

    section = "## 3. Urgent Gaps - Detailed Analysis\n\n"
    section += f"The following {len(urgent_gaps)} capabilities require immediate attention:\n\n"

    for cap in urgent_gaps:
        # Find capability in knowledge base
        kb_cap = find_capability_in_kb(cap['capability_id'], knowledge_base)
        if not kb_cap:
            continue

        # Format context and synthesize with Claude
        context = format_gap_context(cap, kb_cap)
        synthesis = synthesize_with_claude("urgent_gap", context, VALID_AGENTS)

        section += f"### {cap['capability_name']}\n"
        section += f"**Phase:** {cap['phase_name']} | "
        section += f"**Scores:** I={cap['importance']}, R={cap['readiness']}, Gap={cap['gap_score']}\n\n"
        section += synthesis + "\n\n"
        section += "---\n\n"

    return section


def generate_strengths_section(strengths: List[Dict], knowledge_base: dict) -> str:
    """Generate strengths section using Claude synthesis."""
    if not strengths:
        return "## 4. Strengths to Protect\n\nNo major strengths identified (High I + High R).\n\n---\n\n"

    section = "## 4. Strengths to Protect\n\n"
    section += f"The following {len(strengths)} capabilities are organizational strengths to maintain and enhance:\n\n"

    for cap in strengths:
        kb_cap = find_capability_in_kb(cap['capability_id'], knowledge_base)
        if not kb_cap:
            continue

        # Format context and synthesize with Claude
        context = format_strength_context(cap, kb_cap)
        synthesis = synthesize_with_claude("strength", context, VALID_AGENTS)

        section += f"### {cap['capability_name']}\n"
        section += f"**Phase:** {cap['phase_name']} | "
        section += f"**Scores:** I={cap['importance']}, R={cap['readiness']}\n\n"
        section += synthesis + "\n\n"
        section += "---\n\n"

    return section


def find_capability_in_kb(cap_id: str, knowledge_base: dict) -> dict:
    """Find capability in knowledge base by ID."""
    for phase in knowledge_base.get('phases', []):
        for cap in phase.get('capabilities', []):
            if cap.get('id') == cap_id:
                return cap
    return None


def validate_report(report_text: str) -> List[str]:
    """
    Validate report only flags INVENTED agent names, not general AI references.

    We're checking that when the report references a specific agent by name,
    it's one that actually exists. We're NOT flagging general mentions of
    AI, GenAI, or descriptive text like "USB for AI".
    """
    warnings = []

    # Pattern to find likely agent name references (capitalized, followed by Agent/Bot)
    # This looks for patterns like "Something Agent" or "Something Bot" that appear
    # to be naming a specific agent
    agent_name_pattern = r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(Agent|Bot)\b'

    matches = re.findall(agent_name_pattern, report_text)

    for match in matches:
        full_name = f"{match[0]} {match[1]}"
        # Check if this looks like an agent name but isn't in our list
        if full_name not in VALID_AGENTS:
            # Skip known false positives (section titles, generic terms)
            skip_phrases = [
                "First Zuora Agent",  # Section title
                "Your First Zuora Agent",
                "Building Your First Agent",
                "AI Agent",  # Generic term
                "MCP Agent",  # Generic term
                "Custom Agent",  # Generic term
                "Business Agent",  # Generic category
                "The Agent",  # Generic reference
            ]
            if full_name not in skip_phrases:
                warnings.append(f"⚠️ Unknown agent referenced: '{full_name}'")

    # Check for speculative language
    speculative_phrases = [
        "could potentially",
        "might be able to",
        "we recommend exploring",
        "consider implementing",
        "it's possible that",
        "you should consider",
        "we suggest",
    ]

    for phrase in speculative_phrases:
        if phrase.lower() in report_text.lower():
            warnings.append(f"⚠️ Speculative language detected: '{phrase}'")

    return warnings


def create_quick_summary(analyzed_capabilities: List[Dict]) -> str:
    """
    Create a quick text summary of the assessment results.
    """
    priority_matrix = create_priority_matrix(analyzed_capabilities)
    urgent_gaps = get_capabilities_by_category(analyzed_capabilities, "URGENT_GAP")
    strengths = get_capabilities_by_category(analyzed_capabilities, "STRENGTH")

    summary = f"""
## Quick Assessment Summary

**Total Capabilities Assessed:** {len(analyzed_capabilities)}

**Priority Distribution:**
- 🔴 Urgent Gaps: {priority_matrix['URGENT_GAP']}
- 🟠 Critical Gaps: {priority_matrix['CRITICAL_GAP']}
- 🟢 Strengths: {priority_matrix['STRENGTH']}
- 🟡 Opportunities: {priority_matrix['OPPORTUNITY']}
- 🔵 Maintain: {priority_matrix['MAINTAIN']}
- ⚪ Deprioritize: {priority_matrix['DEPRIORITIZE']}

**Top Urgent Gaps:**
"""

    for i, cap in enumerate(urgent_gaps[:5], 1):
        summary += f"\n{i}. **{cap['capability_name']}** ({cap['phase_name']})"
        summary += f"\n   - Importance: {cap['importance']}, Readiness: {cap['readiness']}"
        summary += f"\n   - Gap Score: {cap['gap_score']}"

    summary += "\n\n**Top Strengths:**\n"

    for i, cap in enumerate(strengths[:5], 1):
        summary += f"\n{i}. **{cap['capability_name']}** ({cap['phase_name']})"
        summary += f"\n   - Importance: {cap['importance']}, Readiness: {cap['readiness']}"

    return summary
