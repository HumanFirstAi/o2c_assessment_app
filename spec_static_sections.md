# SPEC: Static Report Sections (MCP Guide)

## Overview

These sections are STATIC TEXT - no LLM generation needed.
Copy these directly into the report generator as constants.

---

## MCP_GUIDE_SECTION Constant

```python
MCP_GUIDE_SECTION = """
### What MCP Gives You

MCP (Model Context Protocol) is a standard way for AI tools (Claude Desktop, Cursor, 
ChatGPT Codex, etc.) to plug into external systems – think of it as USB for AI.

The Developer MCP Server lets AI tools:
- Query your tenant (accounts, subscriptions, invoices, etc.)
- Generate SDK code in Java, Python, Node.js, C#, curl
- Ask product questions ("How do I implement usage-based billing?")
- Help with SDK upgrades
- Create catalog & subscriptions (with approval controls)

You run this MCP server on your own machine; your AI client connects securely 
using your OAuth client credentials.

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
```

---

## AGENT_GUIDE_SECTION Constant

```python
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
```

---

## Usage in report_generator.py

```python
# At top of file, define constants
MCP_GUIDE_SECTION = """..."""  # Copy from above
AGENT_GUIDE_SECTION = """..."""  # Copy from above

# In generate_report function, use directly:
report = f"""
...

## 5. Getting Started with Zuora MCP

{MCP_GUIDE_SECTION}

---

## 6. Building Your First Zuora Agent

{AGENT_GUIDE_SECTION}
"""
```

No LLM calls for these sections - they are static reference material.
