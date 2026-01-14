# SPEC UPDATE: Factual Report Generation

## Overview

This update constrains the report generator to be **strictly factual** - no LLM invention.
It also restructures the report sections and adds the MCP implementation guide.

---

## REVISED REPORT STRUCTURE

### OLD Structure (Remove sections 6-9):
~~1. Executive Summary~~
~~2. Priority Matrix Analysis~~
~~3. Urgent Gaps Detail~~
~~4. Strengths to Protect~~
~~5. Phase-by-Phase Recommendations~~
~~6. AI Agent Roadmap~~ ❌ REMOVE
~~7. MCP Integration Plan~~ ❌ REMOVE  
~~8. Implementation Timeline~~ ❌ REMOVE
~~9. Next Steps~~ ❌ REMOVE

### NEW Structure:

```
1. Executive Summary
2. Priority Matrix Analysis  
3. Urgent Gaps - Detailed Analysis
4. Strengths to Protect
5. What's Available Today (per capability)
6. What's Coming (per capability, from KB)
7. Getting Started with Zuora MCP
8. Building Your First Zuora Agent
```

---

## SECTION SPECIFICATIONS

### Section 1: Executive Summary
**Source:** Computed from scores only
- Count of urgent gaps, critical gaps, strengths
- Top 3 priority capabilities (highest gap score)
- Overall readiness score (average R across all capabilities)
- NO invented recommendations - just facts

### Section 2: Priority Matrix Analysis  
**Source:** Computed from scores only
- Counts by category (URGENT_GAP, CRITICAL_GAP, etc.)
- Distribution by phase
- Visual matrix or table

### Section 3: Urgent Gaps - Detailed Analysis
**Source:** ONLY from knowledge_base.json fields

For each URGENT_GAP capability, output EXACTLY:

```markdown
### [Capability Name]
**Phase:** [from grid_layout.py]
**Scores:** Importance: [I], Readiness: [R], Gap Score: [calculated]

**Why This Matters:**
[VERBATIM from knowledge_base.json → capability.why_it_matters]

**What's Available Today:**
[VERBATIM from knowledge_base.json → capability.how_it_works_today]

**Platform Features:**
[BULLET LIST from knowledge_base.json → capability.current_ai_capabilities.platform_features]

**AI Agents That Can Help:**
[BULLET LIST from knowledge_base.json → capability.current_ai_capabilities.ai_agents]
- Primary: [from capability.agent_mapping.primary_agents]
- Supporting: [from capability.agent_mapping.supporting_agents]

**MCP Tools Available:**
[BULLET LIST from knowledge_base.json → capability.current_ai_capabilities.mcp_tools]

**What's Coming:**
- Timeline: [from capability.whats_coming.timeline]
- Capabilities: [BULLET LIST from capability.whats_coming.capabilities]
```

### Section 4: Strengths to Protect
**Source:** ONLY from knowledge_base.json

For each STRENGTH (High I + High R), output:
- Capability name and phase
- Why it matters (from KB)
- Current AI capabilities supporting this strength
- Recommendation: "Continue leveraging [agent names from KB]"

### Section 5: What's Available Today
**Source:** Aggregated from knowledge_base.json

Group by availability:
```markdown
## Platform Features Live Now
[List all platform_features across scored capabilities]

## AI Agents Available Now
[List from agent_inventory, only those mapped to scored capabilities]

## MCP Tools Ready to Use
[List all mcp_tools across scored capabilities]
```

### Section 6: What's Coming
**Source:** ONLY from knowledge_base.json whats_coming fields

Group by timeline:
```markdown
## Coming in 0-6 Months (NOW)
[capabilities where whats_coming.timeline = "NOW" or "NOW-6M"]

## Coming in 6-12 Months (NEAR)
[capabilities where whats_coming.timeline = "6-12M"]

## Coming in 12-24 Months (LATER)
[capabilities where whats_coming.timeline = "12-24M"]
```

### Section 7: Getting Started with Zuora MCP
**Source:** STATIC TEXT (from MCP implementation guide - verbatim)

```markdown
## Getting Started with Zuora MCP

### What MCP + Zuora MCP Gives You

MCP (Model Context Protocol) is a standard way for AI tools (Claude Desktop, Cursor, 
ChatGPT Codex, etc.) to plug into external systems like Zuora – think of it as USB for AI.

The Zuora Developer MCP Server (zuora-mcp on npm) lets AI tools:
- Query your Zuora tenant (accounts, subscriptions, invoices, etc.)
- Generate SDK code for Zuora in Java, Python, Node.js, C#, curl
- Ask product questions ("How do I implement usage-based billing?")
- Help with SDK upgrades
- Create catalog & subscriptions (with approval controls)

You run this MCP server on your own machine; your AI client connects securely 
using your Zuora OAuth client credentials.

### Prerequisites

You'll need:
- A Zuora tenant (ideally sandbox/test for first setup)
- OAuth client credentials from Zuora:
  - BASE_URL – your REST endpoint (e.g., https://rest.apisandbox.zuora.com)
  - ZUORA_CLIENT_ID and ZUORA_CLIENT_SECRET – created by a Zuora admin
- Node.js and npm installed

### Installation

```bash
node --version   # confirm Node is installed
npm install -g zuora-mcp
```

### Configuration for Claude Desktop

1. Open Claude Desktop settings: Claude → Settings… → Developer tab
2. Click Edit Config to open claude_desktop_config.json
3. Add the mcpServers section:

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

4. Quit Claude Desktop completely and restart

### Configuration for Cursor

1. Go to Settings → Cursor Settings → Tools & MCP → "New MCP Server"
2. Use the same configuration as above
3. Restart Cursor

### Configuration for Windsurf

1. Edit ~/.codeium/windsurf/mcp_config.json
2. Use the same configuration structure
3. Restart Windsurf

### Available MCP Tools

Once connected, these tools are available:

| Tool | Purpose |
|------|---------|
| **zuora_codegen** | Generate SDK code (Java, Python, Node.js, C#, curl) |
| **ask_zuora** | Product knowledge Q&A over Zuora docs |
| **sdk_upgrade** | Plan and execute SDK upgrades |
| **query_objects** | Query 40+ Zuora object types with filters |
| **create_product** | Create products (with approval) |
| **create_product_rate_plan** | Create rate plans (with approval) |
| **create_product_rate_plan_charge** | Create charges (with approval) |
| **create_subscription** | Create subscriptions via Order API (with approval) |

### Sanity Check

Test with a safe, read-only query:
```
"list all the euro billing accounts"
```

### Troubleshooting

| Issue | Solution |
|-------|----------|
| Command not found: npx | Node/npm not installed or PATH issue |
| Authentication failed | Check BASE_URL, CLIENT_ID, CLIENT_SECRET |
| Cannot find module 'zuora-mcp' | Run: npm install -g zuora-mcp |
| Tools not appearing | Check JSON syntax, restart app fully |
```

### Section 8: Building Your First Zuora Agent
**Source:** STATIC TEXT (from MCP implementation guide)

```markdown
## Building Your First Zuora Agent

### Option 1: Use Existing Tools as Agents (No Engineering)

Once MCP is configured, Claude Desktop or Cursor become Zuora-aware agents:

**In Claude Desktop:**
```
"Generate Java SDK code to create a subscription with annual billing 
and a usage add-on, using Zuora best practices."
```
Claude will call zuora_codegen and return working code.

**In Cursor:**
```
"List all active subscriptions for account A-0000123 created in the last 90 days."
```
Cursor uses query_objects via Zuora MCP and returns actual tenant data.

**For SDK Upgrades:**
```
"Help me upgrade from Zuora Java SDK v3.5.0 to v3.6.0; what changed?"
```
The client calls sdk_upgrade and presents changelogs and breaking changes.

### Option 2: Build Custom Agents

To embed a Zuora-aware agent in your own applications:

1. **Pick an agent host that speaks MCP**
   - Claude, Codex, or custom orchestrator

2. **Define the agent's job**
   - Example: "Billing Account Explainer" - explains balance changes
   - Example: "Catalog Assistant" - proposes and creates products with approval

3. **Wire to Zuora MCP**
   - Start: npx -y zuora-mcp
   - Pass: BASE_URL, ZUORA_CLIENT_ID, ZUORA_CLIENT_SECRET

4. **Enforce safety rules**
   - Default to read-only queries
   - Keep approval policies enabled for writes
   - Log key actions

### Best Practices

- **Start in sandbox** for any tools that write data
- **Keep approval enabled** in production
- **Treat MCP server** like any privileged integration (credentials, audit, change management)
- **Start narrow** - one workflow first, then expand

### Getting Access

The Zuora Developer MCP server is in beta. Contact your Zuora CSM or Support for:
- Access to the MCP Server beta
- Latest setup guide PDF
- MCP enablement deck
```

---

## REPORT GENERATOR CONSTRAINTS

### System Prompt for LLM

```python
REPORT_SYSTEM_PROMPT = """
You are generating a strategic assessment report. You must ONLY use information 
from the provided knowledge base. You are a librarian, not an inventor.

ABSOLUTE RULES:
1. NEVER invent agent names - only use names from the provided agent_inventory
2. NEVER speculate about features not documented in the knowledge base
3. NEVER create novel recommendations - only suggest what's documented
4. ALWAYS quote or closely paraphrase the knowledge base text
5. If information is not in the KB, say "Not currently documented"

VALID AGENT NAMES (only reference these):
{agent_list}

For each capability analysis:
- why_it_matters: Use VERBATIM from KB
- how_it_works_today: Use VERBATIM from KB  
- platform_features: List EXACTLY from KB
- ai_agents: List EXACTLY from KB
- mcp_tools: List EXACTLY from KB
- whats_coming: Use EXACTLY from KB with timeline

Your role is to ORGANIZE and PRESENT the knowledge base content based on the 
customer's scores, not to generate new content.
"""
```

### Valid Agent Names (extract from KB)

```python
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
    "Quote Agent / Deal Assist",
    
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
```

### Output Validation

```python
def validate_report(report_text: str) -> list[str]:
    """Validate report only references valid agents."""
    warnings = []
    
    # Check for agent mentions not in valid list
    agent_pattern = r'\b\w+\s+(Agent|Bot|AI|MCP)\b'
    mentions = re.findall(agent_pattern, report_text)
    
    for mention in mentions:
        if mention not in VALID_AGENTS:
            warnings.append(f"Unknown agent referenced: {mention}")
    
    # Check for speculative language
    speculative_phrases = [
        "could potentially",
        "might be able to", 
        "we recommend exploring",
        "consider implementing",
        "it's possible that",
    ]
    for phrase in speculative_phrases:
        if phrase.lower() in report_text.lower():
            warnings.append(f"Speculative language detected: '{phrase}'")
    
    return warnings
```

---

## IMPLEMENTATION APPROACH

The report should be generated in this order:

1. **Compute scores** - Pure calculation, no LLM
2. **Extract KB content** - Pull relevant fields for each scored capability
3. **Assemble sections 1-6** - Template-based with KB content insertion
4. **Add sections 7-8** - Static MCP guide text (no LLM needed)
5. **Validate output** - Check agent names against valid list
6. **Format for export** - DOCX/PDF/Markdown

### Minimal LLM Usage

The LLM should ONLY be used for:
- Generating the Executive Summary paragraph (constrained to computed facts)
- Formatting/organizing the KB content into readable prose

The LLM should NOT be used for:
- Generating recommendations
- Suggesting timelines
- Naming agents or tools
- Speculating about capabilities

---

## FILE CHANGES REQUIRED

### Update: modules/report_generator.py

1. Add VALID_AGENTS constant
2. Add MCP_GUIDE_TEXT constant (sections 7-8)
3. Update system prompt with constraints
4. Add validation function
5. Change report sections per new structure
6. Make sections 3-6 template-based (KB field insertion)

### Update: knowledge_base.json (if needed)

Ensure all capabilities have complete fields:
- why_it_matters
- how_it_works_today
- current_ai_capabilities.platform_features
- current_ai_capabilities.ai_agents
- current_ai_capabilities.mcp_tools
- whats_coming.timeline
- whats_coming.capabilities
- agent_mapping.primary_agents
- agent_mapping.supporting_agents

---

## EXAMPLE OUTPUT (Section 3)

```markdown
### Dunning and Payment Retry
**Phase:** Collect
**Scores:** Importance: 9, Readiness: 3, Gap Score: 6.3

**Why This Matters:**
Traditional dunning is template-based not personalized, reactive and slow, 
and hard to optimize against both recovery rate and churn risk.

**What's Available Today:**
Payment failures trigger alerts. Notification AI Bot summarizes which customers 
and amounts are impacted and may call standard procedures (retry logic, dunning 
workflow entry, or CS handoff). Collections products handle multi-step dunning 
and retry policies; AI is starting to optimize who goes into which path.

**Platform Features:**
- GenAI + Predictive AI collections workflow hub that sorts customers into 
  automated dunning + CC retry flows or priority queues for agents
- Proactive collections chatbot that engages customers to show simplified 
  bills and collect payment in their preferred channel/method

**AI Agents That Can Help:**
- Primary: Notification AI Bot, Collections Manager Agent
- Supporting: Customer Health Agent

**MCP Tools Available:**
- Sort customers into automated dunning vs priority queues
- Trigger dunning workflow entry or CS handoff
- Summarize which customers and amounts are impacted

**What's Coming:**
- Timeline: 6-12M
- Capabilities:
  - Adaptive dunning strategies using customer value, engagement history, 
    and credit risk
  - Agent-driven customer interaction explaining failed payments in plain 
    language and proposing easy actions
```

This is 100% from the knowledge base - no invention.
