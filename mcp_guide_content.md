# Zuora MCP Implementation Guide

This content is included in generated reports as Sections 7-8.

## Section 7: Getting Started with Zuora MCP

### What MCP + Zuora MCP Gives You

MCP (Model Context Protocol) is a standard way for AI tools (Claude Desktop, Cursor, ChatGPT Codex, etc.) to plug into external systems like Zuora – think of it as USB for AI.

The Zuora Developer MCP Server (zuora-mcp on npm) lets AI tools:
- Query your Zuora tenant (accounts, subscriptions, invoices, etc.)
- Generate SDK code for Zuora in Java, Python, Node.js, C#, curl
- Ask product questions ("How do I implement usage-based billing?")
- Help with SDK upgrades
- Create catalog & subscriptions (with approval controls)

You run this MCP server on your own machine; your AI client connects securely using your Zuora OAuth client credentials.

### Prerequisites

You'll need:
- A Zuora tenant (ideally sandbox/test for first setup)
- OAuth client credentials from Zuora:
  - BASE_URL – your REST endpoint (e.g., https://rest.apisandbox.zuora.com)
  - ZUORA_CLIENT_ID and ZUORA_CLIENT_SECRET – created by a Zuora admin
- Node.js and npm installed

**Recommendation:** Start in a non-production Zuora environment until you're comfortable with the tools that can modify data.

### Installation

```bash
node --version   # confirm Node is installed
npm install -g zuora-mcp
```

The MCP server package is publicly available at https://www.npmjs.com/package/zuora-mcp

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
5. In the Developer section you should see Zuora MCP listed as a running MCP server

### Configuration for Cursor

1. Go to Settings → Cursor Settings → Tools & MCP → "New MCP Server"
2. Configure with the same JSON structure as above
3. Restart Cursor and verify no errors; you should see the Zuora MCP server active

### Configuration for Windsurf

1. Edit ~/.codeium/windsurf/mcp_config.json
2. Use the same configuration structure
3. Save and restart Windsurf

### Configuration for OpenAI Codex CLI

1. Install the CLI: `npm i -g @openai/codex`
2. Edit ~/.codex/config.toml and add:

```toml
[mcp_servers.zuora-mcp]
command = "npx"
args = ["-y", "zuora-mcp"]

[mcp_servers.zuora-mcp.env]
BASE_URL = "https://rest.apisandbox.zuora.com"
ZUORA_CLIENT_ID = "your-client-id"
ZUORA_CLIENT_SECRET = "your-client-secret"
```

3. Start Codex CLI, type /mcp, and confirm Zuora MCP is listed

### Available MCP Tools

Once connected, these tools are available:

| Tool | Purpose |
|------|---------|
| **zuora_codegen** | Generate integration code using Zuora's SDKs (Java, Python, Node.js, C#, curl) |
| **ask_zuora** | Product knowledge Q&A over Zuora docs |
| **sdk_upgrade** | Plan and execute SDK upgrades with changelogs and breaking changes |
| **query_objects** | Query 40+ Zuora object types with filters (NE, LT, GT, GE, LE, SW, IN) |
| **create_product** | Create products (governed by approval policy) |
| **create_product_rate_plan** | Create rate plans (governed by approval policy) |
| **create_product_rate_plan_charge** | Create charges (governed by approval policy) |
| **create_subscription** | Create subscriptions via Order API (governed by approval policy) |

### Sanity Check

Test with a safe, read-only query in your MCP client:

```
"list all the euro billing accounts"
```

The MCP server will interpret that as "query BillingAccounts where currency = EUR" and return a table of accounts.

### Troubleshooting

| Issue | Solution |
|-------|----------|
| Command not found: npx | Node/npm not installed or PATH issue |
| Authentication failed | Check BASE_URL, CLIENT_ID, CLIENT_SECRET and environment (sandbox vs production) |
| Cannot find module 'zuora-mcp' | Reinstall globally: npm install -g zuora-mcp |
| Tools not appearing | Often JSON syntax error or wrong config file path; restart app fully |

---

## Section 8: Building Your First Zuora Agent

### Option 1: Use Existing Tools as Agents (No Engineering Required)

Once MCP is configured, Claude Desktop or Cursor become Zuora-aware agents. This is the fastest path to getting started.

**Code Generation Example (Claude Desktop):**
```
"Generate Java SDK code to create a subscription with annual billing 
and a usage add-on, using Zuora best practices."
```
Claude will call zuora_codegen, then refine with code_rules and API/model details.

**Data Query Example (Cursor):**
```
"List all active subscriptions for account A-0000123 created in the last 90 days."
```
Cursor will use the query_objects tool via Zuora MCP and return actual data from your tenant.

**SDK Upgrade Example:**
```
"Help me upgrade from Zuora Java SDK v3.5.0 to v3.6.0; what changed and how should I refactor this code file?"
```
The client will call sdk_upgrade and present upgrade steps, changelogs, and any breaking changes.

### Option 2: Build Custom Agents

To embed a Zuora-aware agent in your own applications (support portal chatbot, ops console, internal engineering tool):

**Step 1: Pick or build an agent host that speaks MCP**
- Many modern frameworks and tools already support MCP
- You can also connect to MCP servers yourself using the open protocol

**Step 2: Define the agent's job, not just its tools**

Example personas:
- **Billing Account Explainer** – Given an account ID, explain why the balance has changed using invoices, payments, and subscriptions queried via MCP
- **Catalog Assistant** – Propose and create new products/rate plans using create_product and related tools, with human approval in the loop
- **Integration Helper** – Generate and test SDK code for specific use cases

**Step 3: Wire your orchestrator to Zuora MCP**

Configure your orchestrator to:
- Start the zuora-mcp command: `npx -y zuora-mcp`
- Pass environment variables: BASE_URL, ZUORA_CLIENT_ID, ZUORA_CLIENT_SECRET

Then define prompts/instructions so your agent:
- Uses zuora_codegen when it needs code
- Uses query_objects for data
- Uses catalog/subscription tools only after confirming with the user

**Step 4: Enforce environment & safety rules**

Production agents should:
- Default to read-only queries unless explicitly approved
- Keep approval policies turned on when writing to Zuora
- Log or audit key actions (created product SKUs, subscriptions created by the agent)

**Step 5: Iterate and expand**

Start with a single, narrow workflow:
- Example: "Agent helps developers build and test a new integration in a week using zuora_codegen and sdk_upgrade tools"

Over time:
- Add more MCP tools
- Switch from local to centralized deployment (running zuora-mcp on a shared internal host with your own auth and logging)

### Best Practices for Production Agents

| Practice | Description |
|----------|-------------|
| **Start in sandbox** | Use sandbox for any tools that write data |
| **Keep approval enabled** | Treat the MCP server like any privileged integration |
| **Audit key actions** | Log product SKUs, subscriptions, and modifications |
| **Credential management** | Secure your CLIENT_ID and CLIENT_SECRET |
| **Change management** | Follow your standard deployment processes |

### Getting Access

The Zuora Developer MCP server is in beta and is already being used by a number of tenants.

To get started:
- Contact your Zuora CSM or Zuora Support
- Request access to the MCP Server beta
- Ask for the latest "Zuora MCP setup for Desktop Clients" guide (PDF)
- Request the MCP enablement deck
