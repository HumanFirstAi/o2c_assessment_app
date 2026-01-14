# O2C AI Agent & MCP Readiness Assessment App

## Specification for Claude Code CLI Build

---

## 1. PROJECT OVERVIEW

### 1.1 Purpose
Build a Streamlit application that:
1. Accepts an uploaded image of a completed Lifecycle Assessment (with I/R scores 1-10)
2. Uses vision/OCR to extract scores for each capability
3. Generates a strategic priority guide and guidance document based on the scores + AI/MCP knowledge base

### 1.2 Core Value Proposition
Transform a static paper-based assessment into an intelligent, AI-powered strategic roadmap that maps capability gaps to specific Zuora AI agents and MCP capabilities.

---

## 2. ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────┐
│                     STREAMLIT APPLICATION                        │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────────────┐  │
│  │   Image     │  │   Score      │  │   Report Generator     │  │
│  │   Upload    │──│   Extractor  │──│   (LLM + Knowledge)    │  │
│  │   Module    │  │   (Vision)   │  │                        │  │
│  └─────────────┘  └──────────────┘  └────────────────────────┘  │
│         │                │                      │                │
│         ▼                ▼                      ▼                │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │              KNOWLEDGE BASE (JSON/YAML)                     ││
│  │   - 8 Phases, 45 Capabilities                               ││
│  │   - AI Agent mappings per capability                        ││
│  │   - MCP tool mappings per capability                        ││
│  │   - Current state vs Roadmap                                ││
│  └─────────────────────────────────────────────────────────────┘│
│         │                                                        │
│         ▼                                                        │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │              OUTPUT: Strategic Priority Guide               ││
│  │   - Priority Matrix (High I + Low R = Urgent)               ││
│  │   - Capability-to-Agent mapping                             ││
│  │   - Recommended timeline                                     ││
│  │   - Downloadable DOCX/PDF                                    ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. DATA MODEL

### 3.1 Phase Structure

```python
PHASES = [
    {
        "id": "configure_price",
        "name": "Configure and Price",
        "color": "#2E7D32",
        "agentic_goal": "AI-optimized monetization",
        "key_question": "Is our pricing driven by AI simulation and optimization?",
        "capabilities": [...]
    },
    {
        "id": "quote_sell",
        "name": "Quote and Sell",
        "color": "#1565C0",
        "agentic_goal": "Agentic, omnichannel quoting",
        "key_question": "Can any channel create a quote using the same CPQ brain?",
        "capabilities": [...]
    },
    {
        "id": "invoice",
        "name": "Invoice",
        "color": "#7B1FA2",
        "agentic_goal": "Self-healing billing flows",
        "key_question": "How many invoicing errors were flagged and fixed by an agent today?",
        "capabilities": [...]
    },
    {
        "id": "collect",
        "name": "Collect",
        "color": "#00838F",
        "agentic_goal": "Autonomous payment recovery",
        "key_question": "Are failed payments being remediated by a bot before a human is alerted?",
        "capabilities": [...]
    },
    {
        "id": "provision",
        "name": "Provision",
        "color": "#F9A825",
        "agentic_goal": "Instant access & entitlement",
        "key_question": "Is customer access granted automatically via an MCP-governed workflow?",
        "capabilities": [...]
    },
    {
        "id": "recognize_report",
        "name": "Recognize and Report",
        "color": "#6A1B9A",
        "agentic_goal": "Automated compliance summaries",
        "key_question": "Are we using AI to draft our incident and financial compliance summaries?",
        "capabilities": [...]
    },
    {
        "id": "learn",
        "name": "Learn",
        "color": "#EF6C00",
        "agentic_goal": "Closed-loop intelligence",
        "key_question": "Do insights feed back automatically into Configure, Quote, Invoice, Collect?",
        "capabilities": [...]
    },
    {
        "id": "sustain_grow",
        "name": "Sustain and Grow",
        "color": "#1976D2",
        "agentic_goal": "Proactive retention & expansion",
        "key_question": "Are churn risks being addressed before customers leave?",
        "capabilities": [...]
    }
]
```

### 3.2 Capability Structure

```python
CAPABILITY_SCHEMA = {
    "id": str,                    # e.g., "offer_catalog_management"
    "name": str,                  # e.g., "Offer/Catalog Management"
    "subtitle": str,              # e.g., "Price, Usage, Promo"
    "phase_id": str,              # Reference to parent phase
    "row": int,                   # Grid position (1-7)
    "col": int,                   # Grid position (1-8)
    "importance_score": int,      # Extracted from image (1-10)
    "readiness_score": int,       # Extracted from image (1-10)
    "priority_category": str,     # Computed: "urgent_gap", "strength", "deprioritize"
    
    # AI/MCP Knowledge
    "why_it_matters": str,
    "current_ai_capabilities": {
        "platform_features": list[str],
        "ai_agents": list[str],
        "mcp_tools": list[str]
    },
    "how_it_works_today": str,
    "whats_coming": {
        "timeline": str,          # "NOW", "6-12M", "12-24M"
        "capabilities": list[str]
    },
    "agent_mapping": {
        "primary_agents": list[str],
        "supporting_agents": list[str]
    }
}
```

---

## 4. KNOWLEDGE BASE

### 4.1 Complete Capability Definitions

Create a file `knowledge_base.json` with the following structure. Below is the complete content for all 45 capabilities:

```json
{
  "metadata": {
    "version": "1.0",
    "last_updated": "2025-01",
    "framework": "Recurring Revenue Management Lifecycle"
  },
  "mcp_overview": {
    "description": "MCP (Model Context Protocol) acts as the 'USB for AI' that standardizes how agents safely interact with Zuora's catalog, pricing, usage, billing, revenue, and workflow services across the revenue lifecycle.",
    "current_state": {
      "developer_mcp": "Local server for catalog CRUD, pricing configuration, and SDK codegen",
      "remote_mcp_server": "Planned - exposes tools to agents in Glean, Slack, and external LLMs"
    },
    "mcp_gateway": "Single governed interface for partner and customer agents to discover and execute monetization operations"
  },
  "agent_inventory": {
    "concierge_agents": [
      {"name": "Anantha Concierge", "role": "Orchestrates domain-specific agents for unified responses"},
      {"name": "Zuora AI Concierge", "role": "Customer-facing orchestration across billing, revenue, collections"}
    ],
    "business_agents": [
      {"name": "Billing Operations Agent", "role": "Bill-run QA, subscription management, anomaly detection"},
      {"name": "Collections Manager Agent", "role": "Automated collections, priority scoring, script generation"},
      {"name": "Revenue Accountant Agent", "role": "Data quality, reconciliation, revenue explanation"},
      {"name": "Revenue Manager Agent", "role": "Audit prep, financial reporting, multi-year forecasting"},
      {"name": "Customer Success Agent", "role": "Health monitoring, playbook execution, education"},
      {"name": "Customer Health Agent", "role": "Real-time churn risk monitoring and next-best-action"},
      {"name": "Churn Agent", "role": "Behavioral pattern analysis around churn signals"},
      {"name": "Quote Agent / Deal Assist", "role": "Alternative quote scenarios, deal scoring, guidance"}
    ],
    "functional_agents": [
      {"name": "Billing/Invoice Service Agent", "role": "BFD, billing node, invoice diagnostics"},
      {"name": "Mediation/DACO Agent", "role": "Data Connect and mediation troubleshooting"},
      {"name": "DQ/Trino Agent", "role": "Data health checks, query execution, anomaly detection"},
      {"name": "Data Management Agent", "role": "Dynamic validation, real-time anomaly detection"},
      {"name": "RCA Agent", "role": "Root cause analysis drafting with templates"},
      {"name": "Notification AI Bot", "role": "Autonomous alert recognition, impact analysis, remediation"},
      {"name": "Workflow AI Bot", "role": "Encapsulates multi-step playbooks as MCP tools"}
    ],
    "specialized_agents": [
      {"name": "Outcomes Simulation Agent", "role": "What-if simulations for plans, revenue/margin projections"},
      {"name": "Revenue Narrator", "role": "Plain-language explanations of revenue changes"},
      {"name": "SSP Analyzer", "role": "Standalone selling price analysis"},
      {"name": "Query Assistant", "role": "Natural language to validated SQL"},
      {"name": "Reconciliation AI", "role": "Automated subledger to ERP/GL reconciliation"},
      {"name": "DataFix AI", "role": "Diagnose and auto-fix low-risk data issues"}
    ]
  },
  "phases": [
    // PHASE 1: CONFIGURE AND PRICE
    {
      "id": "configure_price",
      "name": "Configure and Price",
      "color": "#2E7D32",
      "agentic_goal": "AI-optimized monetization",
      "strategy_context": "Move from static, hand-coded catalog and pricing setups to an Agentic Monetization Platform where specialist agents handle configuration and optimization work.",
      "capabilities": [
        {
          "id": "offer_catalog_management",
          "name": "Offer/Catalog Management",
          "subtitle": "Price, Usage, Promo",
          "row": 1, "col": 1,
          "why_it_matters": "Catalog, bundles, and offers are the epicenter of Total Monetization. Many customers suffer from SKU sprawl, fragmented offer logic, and duplication across CPQ, storefronts, and billing.",
          "current_ai_capabilities": {
            "platform_features": [
              "Monetization Catalog & Offer Management with unified catalog for products, plans, bundles, promotions",
              "Dynamic, attribute-based promotions driven by customer, lifecycle, channel context"
            ],
            "ai_agents": ["Developer MCP tools for catalog Q&A and setup guidance"],
            "mcp_tools": [
              "Ingest & manage catalog",
              "Create & manage product pricing/plans/rules",
              "Managing product catalog (products, rate plans, charges)",
              "Complex pricing structures (tiered, volume, overage, multi-attribute)"
            ]
          },
          "how_it_works_today": "MCP tools encapsulate catalog operations. AI agents interpret natural language, call MCP tools to generate payloads, validate pricing, and execute catalog changes.",
          "whats_coming": {
            "timeline": "6-12M",
            "capabilities": [
              "GA of Intelligent Merchandising and Promotions Management",
              "AI-driven suggestion of new packages/bundles powered by usage and performance data",
              "Remote MCP Server / MCP Gateway for external agents"
            ]
          },
          "agent_mapping": {
            "primary_agents": ["Developer MCP"],
            "supporting_agents": ["Anantha Concierge"]
          }
        },
        {
          "id": "price_management",
          "name": "Price Management",
          "subtitle": "",
          "row": 2, "col": 1,
          "why_it_matters": "Customers want to innovate pricing models (usage, hybrid, commitments) without exploding SKUs or hard-coding rules in each channel. Pain points include rigid discounting, manual pricing, and high engineering cost to change price books.",
          "current_ai_capabilities": {
            "platform_features": [
              "Dynamic and Attribute-Based Pricing using real-time business context",
              "Context Service feeding channel, customer, location into pricing decisions"
            ],
            "ai_agents": ["Developer MCP for pricing configuration"],
            "mcp_tools": [
              "Configure all pricing charge types (flat, per-unit, tiered, volume, overage, high-watermark, multi-attribute)",
              "Generate example payloads and SDK code"
            ]
          },
          "how_it_works_today": "AI agents read existing charge structures, propose standardized patterns, draft and execute payloads to standardize pricing while keeping human approval in the loop.",
          "whats_coming": {
            "timeline": "6-12M",
            "capabilities": [
              "Rules Engine + merchandising rules for AI-authored pricing policies",
              "Soft bundles and advanced policies (top-up, overage, rollover)",
              "Price/Profit Optimization in Learn phase feeding back targets"
            ]
          },
          "agent_mapping": {
            "primary_agents": ["Developer MCP", "Outcomes Simulation Agent"],
            "supporting_agents": ["Anantha Concierge"]
          }
        },
        {
          "id": "revenue_planning",
          "name": "Revenue Planning",
          "subtitle": "",
          "row": 3, "col": 1,
          "why_it_matters": "Pricing and catalog changes are often made without a forward-looking financial view, leading to missed revenue targets, over/under-monetized usage-based plans, and difficulty justifying changes to Finance.",
          "current_ai_capabilities": {
            "platform_features": ["What-if simulations on any plan with projected billing, revenue, and margin curves"],
            "ai_agents": ["Outcomes Simulation Agent"],
            "mcp_tools": [
              "Pull plan and usage definitions from catalog and usage services",
              "Apply scenario assumptions",
              "Compute projected billing and revenue curves"
            ]
          },
          "how_it_works_today": "The Outcomes Simulation Agent pulls plan definitions via MCP, applies scenario assumptions, computes projections, and returns visualizable data plus plain-language explanations.",
          "whats_coming": {
            "timeline": "12-24M",
            "capabilities": [
              "Tighter linkage with Revenue Manager Agent and Finance Intelligence",
              "Lifecycle-aware planning using Learn-phase signals (churn, expansion)",
              "Autonomous AI-optimized monetization across entry, profit, and retention"
            ]
          },
          "agent_mapping": {
            "primary_agents": ["Outcomes Simulation Agent"],
            "supporting_agents": ["Revenue Manager Agent"]
          }
        },
        {
          "id": "incentive_management",
          "name": "Incentive Management",
          "subtitle": "Rebates, Discounts",
          "row": 4, "col": 1,
          "why_it_matters": "Many customers run promotions and rebates manually or in external tools, struggle to target incentives by lifecycle stage, and have limited feedback loops on which discounts drive profitable growth.",
          "current_ai_capabilities": {
            "platform_features": [
              "Offer Management and Promotion Management with dynamic, attribute-based offers",
              "Stacking, exclusion, conditions, and templates for business users"
            ],
            "ai_agents": ["Developer MCP for offer configuration"],
            "mcp_tools": [
              "Propose incentive structures (trial discounts, lifecycle triggers, volume rebates)",
              "Configure offers and rules",
              "Validate eligibility and simulate financial impact"
            ]
          },
          "how_it_works_today": "AI agents read current promotions via MCP, analyze performance through DQ/insights agents, recommend changes, and push updated offers subject to human approval.",
          "whats_coming": {
            "timeline": "6-12M",
            "capabilities": [
              "AI-driven 'next best incentive' based on behavior and risk",
              "MCP-exposed incentive APIs for partners via MCP Gateway"
            ]
          },
          "agent_mapping": {
            "primary_agents": ["Developer MCP"],
            "supporting_agents": ["Churn Agent", "Customer Health Agent"]
          }
        },
        {
          "id": "channel_management",
          "name": "Channel Management",
          "subtitle": "",
          "row": 5, "col": 1,
          "why_it_matters": "Enterprises sell through multiple channels (storefronts, CPQ, partner portals, marketplaces, AI agents). Without a unified context layer, pricing fragments by channel, partners get inconsistent incentives, and analytics are siloed.",
          "current_ai_capabilities": {
            "platform_features": [
              "Business Context Service / Adaptive Context Service for omnichannel",
              "Commerce Foundation powering packaging, pricing, eligibility across all channels"
            ],
            "ai_agents": ["Channel/partner agents using unified context"],
            "mcp_tools": [
              "MCP Server as 'AI port' across channels",
              "MCP Gateway for single interface to monetization logic"
            ]
          },
          "how_it_works_today": "Channel experiences call context services to resolve attributes, use catalog and offer APIs for appropriate assortments, and early MCP-enabled tools allow agents to fetch product data consistently.",
          "whats_coming": {
            "timeline": "12-24M",
            "capabilities": [
              "Agent-led channels as first-class citizens",
              "Partner/Channel Intelligence feeding back performance data",
              "External agents via MCP discovering products and initiating orders"
            ]
          },
          "agent_mapping": {
            "primary_agents": ["Developer MCP", "Anantha Concierge"],
            "supporting_agents": []
          }
        }
      ]
    },
    // PHASE 2: QUOTE AND SELL
    {
      "id": "quote_sell",
      "name": "Quote and Sell",
      "color": "#1565C0",
      "agentic_goal": "Agentic, omnichannel quoting",
      "strategy_context": "NextGen Zuora CPQ is being built as an AI-first, MCP-compliant CPQ where sales reps, partners, and customers can 'quote anywhere' against a single catalog, pricing, and contract brain.",
      "capabilities": [
        {
          "id": "opportunity_capture",
          "name": "Opportunity Capture",
          "subtitle": "eCommerce, CRM, Partners",
          "row": 1, "col": 2,
          "why_it_matters": "Opportunity-to-quote flows are often brittle: tightly coupled to one CRM, manually re-keyed from eCommerce, or disconnected from partner channels.",
          "current_ai_capabilities": {
            "platform_features": [
              "CPQ 'quote anywhere' architecture with CRM-agnostic APIs",
              "Late-bound price evaluation resolved at quote time",
              "Auto-gen Renewal Quotes and mix quotes (new, amend, renew)"
            ],
            "ai_agents": ["Quote Agent", "Account Insights"],
            "mcp_tools": [
              "Pull pricing rules (GET /catalog/price-rules)",
              "Fetch and mutate quotes (GET /quote/{id}, PATCH /quote, POST /order)",
              "Simulate quote-to-order flows"
            ]
          },
          "how_it_works_today": "CRM/eCommerce surfaces sync opportunities with CPQ. AI quote agent reads opportunity context via MCP, proposes a quote with dynamic pricing, hands draft back to CPQ for human review.",
          "whats_coming": {
            "timeline": "6-12M",
            "capabilities": [
              "JSON-based quote definition language designed for LLM generation",
              "CRM/eCommerce/partner agents creating quotes via declarative spec",
              "Deeper integration of revenue/collections insights into CPQ rules"
            ]
          },
          "agent_mapping": {
            "primary_agents": ["Quote Agent / Deal Assist"],
            "supporting_agents": ["Account Insights", "Revenue agents"]
          }
        },
        {
          "id": "customer_partner_portals",
          "name": "Customer and Partner Portals",
          "subtitle": "",
          "row": 2, "col": 2,
          "why_it_matters": "Growth motions increasingly start in self-serve. Historically, self-serve portals and CPQ used different product/price logic, causing inconsistent offers and manual reconciliation.",
          "current_ai_capabilities": {
            "platform_features": [
              "Hosted Checkout, Embedded Checkout, Self-Serve Portal",
              "Widget libraries for embedding customer experiences",
              "Z-CPQ Portal with widgets for partners"
            ],
            "ai_agents": ["Customer-facing agents in portals"],
            "mcp_tools": [
              "Read usage, entitlements, current subscriptions",
              "Recommend upgrades/add-ons and create quote requests"
            ]
          },
          "how_it_works_today": "Portal and partner widgets rely on MCP-enabled catalog and CPQ services. Customer agents can read context and recommend upgrades; partner agents can build SPRs and apply rules.",
          "whats_coming": {
            "timeline": "6-12M",
            "capabilities": [
              "Omnichannel commerce APIs sharing same context, catalog, and decision services",
              "AI-guided 'quote request to assisted quote' flows for self-serve users"
            ]
          },
          "agent_mapping": {
            "primary_agents": ["Customer Portal Agent", "Partner Agent"],
            "supporting_agents": ["Quote Agent"]
          }
        },
        {
          "id": "guided_selling",
          "name": "Guided Selling",
          "subtitle": "CPQ, Price Guidance",
          "row": 3, "col": 2,
          "why_it_matters": "Complex subscription deals involve many product combinations, ramps, commitments, and non-obvious margin/rev-rec implications. Reps need guided, policy-aware quoting.",
          "current_ai_capabilities": {
            "platform_features": [
              "Guided Selling: Product Discovery with questionnaire-style recommendations",
              "Dynamic Pricing in CPQ using account and opportunity context",
              "Deal Score, margin, rev rec visualization"
            ],
            "ai_agents": ["Deal Assist / Deal Sense Agent", "Quote Agent"],
            "mcp_tools": [
              "Pull configuration rules and price rules",
              "Simulate quote alternatives",
              "Validate policy compliance"
            ]
          },
          "how_it_works_today": "AI Deal Assist creates alternative quote scenarios staying within financial and product boundaries. Smart Guided Selling dynamically adapts discovery paths and surfaces recommendations.",
          "whats_coming": {
            "timeline": "6-12M",
            "capabilities": [
              "Deeper 'agent-in-the-loop' selling with continuous deal scoring",
              "Conversational suggestions for deal improvements",
              "Guided selling success/failure data feeding back into optimization"
            ]
          },
          "agent_mapping": {
            "primary_agents": ["Deal Assist / Deal Sense Agent"],
            "supporting_agents": ["Quote Agent", "Revenue Manager Agent"]
          }
        },
        {
          "id": "customer_risk_fraud",
          "name": "Customer Risk and Fraud Check",
          "subtitle": "",
          "row": 4, "col": 2,
          "why_it_matters": "High-value B2B deals carry credit risk and fraud/identity risk. Surfacing risk at quote time allows sales and finance to adjust terms before committing.",
          "current_ai_capabilities": {
            "platform_features": [
              "Risk indicator score (1-10) evaluating legal T&Cs, payment history, similar customers, quote complexity",
              "Customer Credit Management signals from Billing & Collect"
            ],
            "ai_agents": ["Risk scoring agents (design stage)"],
            "mcp_tools": [
              "Consume billing/collections history and contract metadata",
              "Contribute risk factors to scoring"
            ]
          },
          "how_it_works_today": "Early/design stage. Risk score is part of CPQ decisioning. AI agents can consume billing/collections history via MCP to contribute to risk scoring.",
          "whats_coming": {
            "timeline": "6-12M",
            "capabilities": [
              "AI-driven risk gating in CPQ approval rules",
              "Guided selling suggesting adjusted terms for high-risk deals",
              "Integration with external fraud/credit engines via MCP Gateway"
            ]
          },
          "agent_mapping": {
            "primary_agents": ["Risk Scoring Agent"],
            "supporting_agents": ["Collections Manager Agent", "Quote Agent"]
          }
        },
        {
          "id": "contract_management",
          "name": "Contract Management",
          "subtitle": "",
          "row": 5, "col": 2,
          "why_it_matters": "Complex subscription contracts span multiple years with amendments, renewals, and commitments. Manual contract management creates audit gaps and slows deal velocity.",
          "current_ai_capabilities": {
            "platform_features": [
              "CPQ contract lifecycle management",
              "Quote-to-contract-to-order flows"
            ],
            "ai_agents": ["Quote Agent for contract context"],
            "mcp_tools": [
              "Read current subscriptions and contracts",
              "Generate proposed quotes including amendments"
            ]
          },
          "how_it_works_today": "CPQ manages contract state. AI agents can read contract context via MCP to inform quoting and renewal strategies.",
          "whats_coming": {
            "timeline": "12-24M",
            "capabilities": [
              "AI-assisted contract analysis and amendment suggestions",
              "Automated contract compliance checking",
              "Natural language contract querying"
            ]
          },
          "agent_mapping": {
            "primary_agents": ["Quote Agent"],
            "supporting_agents": ["Revenue Manager Agent"]
          }
        },
        {
          "id": "inventory_ship_availability",
          "name": "Inventory/Ship Availability",
          "subtitle": "",
          "row": 6, "col": 2,
          "why_it_matters": "For hybrid XaaS businesses (physical + digital + services), quoting must respect inventory pools and availability dates, and reflect realistic ship/activation timelines.",
          "current_ai_capabilities": {
            "platform_features": [
              "Inventory: Visibility, Pools, Management in Commerce",
              "Fulfillment and Ship tied to entitlement and deployment"
            ],
            "ai_agents": ["Quoting agents with availability awareness"],
            "mcp_tools": [
              "Query stock levels, pools, locations",
              "Estimate ship or activation windows",
              "Adjust offers based on availability"
            ]
          },
          "how_it_works_today": "Inventory and fulfillment services form basis for exposing availability data to CPQ and agents.",
          "whats_coming": {
            "timeline": "12-24M",
            "capabilities": [
              "Quote-aware availability integration",
              "AI-guided configuration factoring availability and fulfillment costs",
              "Channel agents offering only what's fulfillable in their region"
            ]
          },
          "agent_mapping": {
            "primary_agents": ["Quote Agent"],
            "supporting_agents": ["Fulfillment Agent"]
          }
        }
      ]
    },
    // PHASE 3: INVOICE
    {
      "id": "invoice",
      "name": "Invoice",
      "color": "#7B1FA2",
      "agentic_goal": "Self-healing billing flows",
      "strategy_context": "Move from manual, ticket-driven billing ops to self-healing billing flows. MCP lets agents safely access billing, invoicing, rating, mediation, and data-quality tools.",
      "capabilities": [
        {
          "id": "order_management",
          "name": "Order Management",
          "subtitle": "",
          "row": 1, "col": 3,
          "why_it_matters": "Order data from CPQ, portals, partners is the source of truth for billing. Historically spread across CRMs, middleware, and Zuora, making AI reasoning about discrepancies difficult.",
          "current_ai_capabilities": {
            "platform_features": [
              "Extensible, callable, composable order orchestration components",
              "Refactored core processes for AI/agent extensibility"
            ],
            "ai_agents": ["Billing Operations Agent", "Invoice Service Agent"],
            "mcp_tools": [
              "Inspect orders, invoices, subscriptions as coherent graph",
              "Trigger order-driven workflows",
              "Replay orchestration steps"
            ]
          },
          "how_it_works_today": "Agents are primarily diagnostic/assistive. Billing/Invoice Agent analyzes problems and recommends fixes. Workflow AI Bot encapsulates playbooks as MCP tools.",
          "whats_coming": {
            "timeline": "6-12M",
            "capabilities": [
              "Standard MCP tools for order orchestration (create/amend, re-orchestrate)",
              "Billing Ops Agents executing fixes safely",
              "Customer-facing agents simulating order impacts before changes"
            ]
          },
          "agent_mapping": {
            "primary_agents": ["Billing Operations Agent"],
            "supporting_agents": ["Invoice Service Agent", "Workflow AI Bot"]
          }
        },
        {
          "id": "billing_invoice",
          "name": "Billing, Invoice",
          "subtitle": "",
          "row": 2, "col": 3,
          "why_it_matters": "Billing operations teams must run complex bill runs reliably, avoid errors that trigger disputes, and explain variance quickly.",
          "current_ai_capabilities": {
            "platform_features": [
              "Unified Data Platform across Commerce + Billing + AR + Revenue",
              "Real-time bill forecasting and simulations"
            ],
            "ai_agents": ["Billing/Invoice Service Agents", "Billing Operations Agent", "Notification AI Bot"],
            "mcp_tools": [
              "Call bill run, invoice, and journal APIs",
              "Pre/post QA checks with anomaly detection",
              "Alert recognition, impact analysis, remediation"
            ]
          },
          "how_it_works_today": "Billing Ops Agent reviews bill runs, runs pre-run QA with anomaly checks, flags issues. Notification AI Bot ingests alerts, summarizes impact, invokes standard playbooks.",
          "whats_coming": {
            "timeline": "6-12M",
            "capabilities": [
              "Scaling from 'assist' to 'self-healing' with auto-skip and targeted re-billing",
              "Bill explanations on demand saving 20+ minutes per customer email"
            ]
          },
          "agent_mapping": {
            "primary_agents": ["Billing Operations Agent", "Notification AI Bot"],
            "supporting_agents": ["Billing/Invoice Service Agents"]
          }
        },
        {
          "id": "rating_charging",
          "name": "Rating and Charging",
          "subtitle": "",
          "row": 3, "col": 3,
          "why_it_matters": "Complex rating (commitments, tiers, FX, multi-entity) is where revenue leakage often hides. Manual configuration and debugging doesn't scale with granular usage models.",
          "current_ai_capabilities": {
            "platform_features": [
              "Callable rating components exposed for AI and workflow reuse",
              "Dynamic & attribute-based pricing flowing into rating"
            ],
            "ai_agents": ["Mediation/DACO Agents", "DQ/Trino Agent"],
            "mcp_tools": [
              "Configuration and troubleshooting of rating/charge models",
              "Identify rating failures or skewed data"
            ]
          },
          "how_it_works_today": "AI is mainly in configuration and troubleshooting. Developer MCP helps set up complex rating models. Mediation/DACO and DQ agents identify rating failures.",
          "whats_coming": {
            "timeline": "12-24M",
            "capabilities": [
              "AI-assisted rating optimization recommendations",
              "Standard MCP tools for rating simulation before deployment",
              "AI-driven implementation for GS/partners"
            ]
          },
          "agent_mapping": {
            "primary_agents": ["Mediation/DACO Agent"],
            "supporting_agents": ["DQ/Trino Agent", "Developer MCP"]
          }
        },
        {
          "id": "usage_data_mediation",
          "name": "Usage Data Mediation",
          "subtitle": "",
          "row": 4, "col": 3,
          "why_it_matters": "For usage/consumption models, garbage in = garbage out. Bad or late mediation leads to mis-rating, bill-run delays, disputes, and revenue restatements.",
          "current_ai_capabilities": {
            "platform_features": [
              "Telco-grade mediation, metering and rating",
              "Basic AI capabilities in mediation"
            ],
            "ai_agents": ["Mediation/DACO Agents"],
            "mcp_tools": [
              "Check if mediation jobs ran as expected",
              "Inspect sample usage feeds and transformed records",
              "Point SREs to misconfigured sources"
            ]
          },
          "how_it_works_today": "Agents check mediation jobs, inspect usage feeds, and help SREs find misconfigurations faster than manual log-hunting.",
          "whats_coming": {
            "timeline": "6-12M",
            "capabilities": [
              "AI-driven mediation health & mapping",
              "Usage anomaly detection with AI-assisted feed mapping",
              "MCP-exposed mediation tools for partner agents"
            ]
          },
          "agent_mapping": {
            "primary_agents": ["Mediation/DACO Agent"],
            "supporting_agents": ["Anantha Concierge", "DQ/Trino Agent"]
          }
        },
        {
          "id": "anomaly_detection",
          "name": "Anomaly Detection",
          "subtitle": "",
          "row": 5, "col": 3,
          "why_it_matters": "Without automation, teams catch anomalies only when customers complain or finance spots variance. Manual review at scale is impossible.",
          "current_ai_capabilities": {
            "platform_features": [
              "Usage anomaly detection",
              "Dynamic validation framework with real-time anomaly detection"
            ],
            "ai_agents": ["DQ/Trino Agent", "Data Management Agent", "Notification AI Bot"],
            "mcp_tools": [
              "Health checks and query reports across data stores",
              "Adaptive thresholds for anomaly detection"
            ]
          },
          "how_it_works_today": "DQ/Trino Agent runs health checks. Data Management Agent provides dynamic validation with adaptive checks. Notification AI Bot handles alerts.",
          "whats_coming": {
            "timeline": "NOW-6M",
            "capabilities": [
              "Proactive anomaly detection before bill runs",
              "Auto-flagging with recommended corrections",
              "Integration with billing forecasting for predictive alerts"
            ]
          },
          "agent_mapping": {
            "primary_agents": ["DQ/Trino Agent", "Data Management Agent"],
            "supporting_agents": ["Notification AI Bot", "Billing Operations Agent"]
          }
        },
        {
          "id": "dispute_prediction",
          "name": "Dispute Prediction",
          "subtitle": "",
          "row": 6, "col": 3,
          "why_it_matters": "Identifying likely billing conflicts before they occur prevents customer escalations and reduces collections burden.",
          "current_ai_capabilities": {
            "platform_features": [
              "Billing and payment history analysis",
              "Pattern recognition in dispute history"
            ],
            "ai_agents": ["DQ/Trino Agent", "Collections Manager Agent"],
            "mcp_tools": [
              "Analyze billing patterns for dispute likelihood",
              "Connect dispute history to invoice characteristics"
            ]
          },
          "how_it_works_today": "Early stage. Agents can analyze billing patterns and dispute history to flag high-risk invoices.",
          "whats_coming": {
            "timeline": "6-12M",
            "capabilities": [
              "Predictive dispute scoring on invoices before sending",
              "Proactive outreach for high-risk invoices",
              "Integration with collections for softer early engagement"
            ]
          },
          "agent_mapping": {
            "primary_agents": ["DQ/Trino Agent"],
            "supporting_agents": ["Collections Manager Agent", "Notification AI Bot"]
          }
        }
      ]
    },
    // PHASE 4: COLLECT
    {
      "id": "collect",
      "name": "Collect",
      "color": "#00838F",
      "agentic_goal": "Autonomous payment recovery",
      "strategy_context": "Move from manual collections workflows to AI-driven prioritization, personalized outreach, and autonomous remediation.",
      "capabilities": [
        {
          "id": "payment_routing",
          "name": "Payment and Routing",
          "subtitle": "",
          "row": 1, "col": 4,
          "why_it_matters": "Handling transaction flows efficiently across payment methods, currencies, and regions is foundational to cash collection.",
          "current_ai_capabilities": {
            "platform_features": [
              "Multi-method, multi-currency payment processing",
              "Smart routing capabilities"
            ],
            "ai_agents": ["Collections agents with payment context"],
            "mcp_tools": [
              "Payment method management",
              "Transaction routing optimization"
            ]
          },
          "how_it_works_today": "Payment infrastructure handles routing. Early AI work focuses on optimizing route selection based on success rates.",
          "whats_coming": {
            "timeline": "6-12M",
            "capabilities": [
              "AI-driven optimal route and retry strategy selection",
              "MCP exposure for customer-facing bots to trigger safe payment actions"
            ]
          },
          "agent_mapping": {
            "primary_agents": ["Collections Manager Agent"],
            "supporting_agents": ["Notification AI Bot"]
          }
        },
        {
          "id": "customer_credit_management",
          "name": "Customer Credit Management",
          "subtitle": "",
          "row": 2, "col": 4,
          "why_it_matters": "Poor visibility into credit risk leads to over-extended customers, rising bad debt, or overly conservative terms that slow growth.",
          "current_ai_capabilities": {
            "platform_features": [
              "Collections and AR modules tracking delinquencies",
              "Unified reporting across billing + payments"
            ],
            "ai_agents": ["Collections agents with credit context"],
            "mcp_tools": [
              "Analyze customer communications and billing situation",
              "Sort customers into automated vs high-touch actions"
            ]
          },
          "how_it_works_today": "Credit management is partially automated via Collections and AR modules. Early AI focuses on which customers to prioritize based on payment probability.",
          "whats_coming": {
            "timeline": "6-12M",
            "capabilities": [
              "Credit-aware agents computing risk scores",
              "Scores feeding into dunning strategies and CPQ risk indicators",
              "MCP exposure for external credit/fraud systems"
            ]
          },
          "agent_mapping": {
            "primary_agents": ["Collections Manager Agent"],
            "supporting_agents": ["Risk Scoring Agent", "Quote Agent"]
          }
        },
        {
          "id": "dunning_payment_retry",
          "name": "Dunning and Payment Retry",
          "subtitle": "",
          "row": 3, "col": 4,
          "why_it_matters": "Traditional dunning is template-based, reactive, and hard to optimize against both recovery rate and churn risk.",
          "current_ai_capabilities": {
            "platform_features": [
              "GenAI + Predictive AI collections workflow hub",
              "Proactive collections chatbot for customer engagement"
            ],
            "ai_agents": ["Notification AI Bot", "Collections Manager Agent"],
            "mcp_tools": [
              "Sort customers into automated dunning vs priority queues",
              "Trigger dunning/retry workflows"
            ]
          },
          "how_it_works_today": "Payment failures trigger alerts. Notification AI Bot summarizes impact and calls standard procedures. Collections products handle multi-step dunning; AI optimizes path assignment.",
          "whats_coming": {
            "timeline": "6-12M",
            "capabilities": [
              "Adaptive dunning strategies using value, engagement, and credit risk",
              "Agent-driven customer interaction explaining failures and proposing actions",
              "Execution of payment method updates via MCP"
            ]
          },
          "agent_mapping": {
            "primary_agents": ["Notification AI Bot", "Collections Manager Agent"],
            "supporting_agents": ["Customer Health Agent"]
          }
        },
        {
          "id": "collections",
          "name": "Collections",
          "subtitle": "",
          "row": 4, "col": 4,
          "why_it_matters": "Collections teams are overloaded manually prioritizing accounts, writing bespoke communications, and reconciling across systems. Prime area for AI as workforce multiplier.",
          "current_ai_capabilities": {
            "platform_features": [
              "GenAI letters and call scripting",
              "Predictive models for non-payment/churn probability"
            ],
            "ai_agents": ["Collections Manager Agent"],
            "mcp_tools": [
              "Generate collection emails and scripts",
              "Route cases to automated vs human flows"
            ]
          },
          "how_it_works_today": "Agents generate collection communications based on invoice/payment history. Workflows route low-value/risk to automated flows, high-impact to human collectors with AI context.",
          "whats_coming": {
            "timeline": "6-12M",
            "capabilities": [
              "Full Collections Copilot with 360° view via MCP",
              "Account scoring by collectability and strategic importance",
              "Auto-suggest and execute low-risk actions under policy",
              "Integration with Dispute Prediction for proactive outreach"
            ]
          },
          "agent_mapping": {
            "primary_agents": ["Collections Manager Agent"],
            "supporting_agents": ["Notification AI Bot", "Customer Health Agent"]
          }
        },
        {
          "id": "partner_settlement",
          "name": "Partner Settlement",
          "subtitle": "Incentives and Payment",
          "row": 5, "col": 4,
          "why_it_matters": "Selling through resellers, distributors, and marketplaces requires complex rebate and revenue share calculations. Manual processes create disputes and poor visibility.",
          "current_ai_capabilities": {
            "platform_features": [
              "Partner/Channel Intelligence in Learn phase",
              "Reconciliation AI between subledgers and ERP/GL"
            ],
            "ai_agents": ["Revenue and AR agents for reconciliation"],
            "mcp_tools": [
              "Access partner accounts and contracts",
              "Access invoices, usage, revenue recognition records"
            ]
          },
          "how_it_works_today": "Partner settlement is primarily rules + reporting-driven. Revenue and AR agents ensure underlying data accuracy before settlements.",
          "whats_coming": {
            "timeline": "12-24M",
            "capabilities": [
              "Partner settlement intelligence combining channel intelligence with AR data",
              "Calculate partner-level revenue shares and rebates",
              "Flag anomalies in partner payouts",
              "MCP-exposed partner APIs for settlement queries"
            ]
          },
          "agent_mapping": {
            "primary_agents": ["Revenue Accountant Agent"],
            "supporting_agents": ["Reconciliation AI", "Data Management Agent"]
          }
        }
      ]
    },
    // PHASE 5: PROVISION
    {
      "id": "provision",
      "name": "Provision",
      "color": "#F9A825",
      "agentic_goal": "Instant access & entitlement",
      "strategy_context": "Move from manual hand-offs between billing and downstream systems to instant, policy-driven access and fulfillment via MCP-governed workflows.",
      "capabilities": [
        {
          "id": "entitlement_management",
          "name": "Entitlement Management",
          "subtitle": "",
          "row": 1, "col": 5,
          "why_it_matters": "For digital and hybrid businesses, entitlements determine which features, content, seats, and environments each customer can use. Foundation for provisioning, upsell, and compliance.",
          "current_ai_capabilities": {
            "platform_features": [
              "Entitlement Management in Monetization Catalog",
              "Features & Entitlements simplifying product creation and provisioning"
            ],
            "ai_agents": ["Developer MCP for entitlement setup"],
            "mcp_tools": [
              "Define and reuse features across products",
              "Automate provisioning based on purchases",
              "Query 'what should this customer be entitled to now?'"
            ]
          },
          "how_it_works_today": "AI assists product teams in defining feature/entitlement structures via MCP and Developer tools.",
          "whats_coming": {
            "timeline": "6-12M",
            "capabilities": [
              "Autonomous entitlement updates on order/contract changes",
              "Customer-facing agents explaining entitlements",
              "Integrated upsell/cross-sell powered by entitlement gaps"
            ]
          },
          "agent_mapping": {
            "primary_agents": ["Developer MCP", "Provisioning Agent"],
            "supporting_agents": ["Anantha Concierge"]
          }
        },
        {
          "id": "inventory",
          "name": "Inventory",
          "subtitle": "",
          "row": 2, "col": 5,
          "why_it_matters": "Tracking physical or digital stock accurately is essential for fulfillment and avoiding over-promising in quotes.",
          "current_ai_capabilities": {
            "platform_features": [
              "Inventory: Visibility, Pools, Management",
              "Integration with fulfillment workflows"
            ],
            "ai_agents": ["Fulfillment/provisioning agents"],
            "mcp_tools": [
              "Query inventory levels and pools",
              "Update availability based on orders"
            ]
          },
          "how_it_works_today": "Inventory services integrated with commerce and fulfillment. AI starting to assist in availability queries.",
          "whats_coming": {
            "timeline": "12-24M",
            "capabilities": [
              "Real-time inventory-aware quoting",
              "AI-driven inventory optimization recommendations"
            ]
          },
          "agent_mapping": {
            "primary_agents": ["Fulfillment Agent"],
            "supporting_agents": ["Quote Agent"]
          }
        },
        {
          "id": "fulfillment_ship",
          "name": "Fulfillment and Ship",
          "subtitle": "",
          "row": 3, "col": 5,
          "why_it_matters": "For hybrid products (physical + digital), digital entitlements must be applied and partners/systems must stay in sync. Manual processes lead to errors.",
          "current_ai_capabilities": {
            "platform_features": [
              "Fulfillment: Drop Ship, Delivery, Order",
              "Integration with external fulfillment systems (e.g., Naviga for print)"
            ],
            "ai_agents": ["Workflow AI concepts for orchestration"],
            "mcp_tools": [
              "Understand subscriptions, orders, entitlements",
              "Initiate or track fulfillment"
            ]
          },
          "how_it_works_today": "Fulfillment driven by workflows and integrations. AI starting to assist in orchestration and GS-led implementation projects.",
          "whats_coming": {
            "timeline": "12-24M",
            "capabilities": [
              "Agent-orchestrated fulfillment workflows",
              "Customer-visible fulfillment intelligence in portal/chat"
            ]
          },
          "agent_mapping": {
            "primary_agents": ["Fulfillment Agent", "Workflow AI Bot"],
            "supporting_agents": ["Anantha Concierge"]
          }
        },
        {
          "id": "deployment_provisioning",
          "name": "Deployment / Provisioning",
          "subtitle": "",
          "row": 4, "col": 5,
          "why_it_matters": "For SaaS and digital products, customers expect instant access after payment. Delays cause dissatisfaction and churn risk. Manual activation creates audit gaps.",
          "current_ai_capabilities": {
            "platform_features": [
              "Provisioning triggered upon payment confirmation",
              "Automatic access grant and de-provisioning"
            ],
            "ai_agents": ["Provisioning Agents", "Infra/DACO Agents"],
            "mcp_tools": [
              "Subscription Management tools",
              "Fulfillments & Delivery Adjustments tools"
            ]
          },
          "how_it_works_today": "Provisioning orchestrated through workflows with triggers from orders/payments. AI agents assist with configuration and troubleshooting.",
          "whats_coming": {
            "timeline": "6-12M",
            "capabilities": [
              "Autonomous provisioning huddles under Anantha orchestration",
              "MCP-governed, tenant-safe activation with full observability"
            ]
          },
          "agent_mapping": {
            "primary_agents": ["Provisioning Agent", "Anantha Concierge"],
            "supporting_agents": ["Infra/DACO Agents"]
          }
        }
      ]
    },
    // PHASE 6: RECOGNIZE AND REPORT
    {
      "id": "recognize_report",
      "name": "Recognize and Report",
      "color": "#6A1B9A",
      "agentic_goal": "Automated compliance summaries",
      "strategy_context": "Move from manual, spreadsheet-heavy close and reporting to AI-assisted, explainable, and auditable revenue operations.",
      "capabilities": [
        {
          "id": "revenue_recognition",
          "name": "Revenue Recognition",
          "subtitle": "",
          "row": 1, "col": 6,
          "why_it_matters": "Revenue accounting teams face complex multi-element, multi-year, consumption-based contracts, SFC requirements, and pressure to close faster while maintaining accuracy.",
          "current_ai_capabilities": {
            "platform_features": [
              "SFC Intelligence (auto-identify SFC contracts, scenario modeling)",
              "Complex Consumption Monetization (FX, multi-entity, usage anomaly detection)"
            ],
            "ai_agents": ["Revenue Accountant Agent", "Revenue Narrator", "Data Management Agent", "Reconciliation AI", "DataFix AI"],
            "mcp_tools": [
              "Access revenue schedules, usage, billing context",
              "Validate transaction staging and contract groupings",
              "Generate period-over-period explanations"
            ]
          },
          "how_it_works_today": "Agents validate staging and groupings, explain revenue movements in natural language, highlight anomalies. Humans remain in control with AI handling narratives and diagnostics.",
          "whats_coming": {
            "timeline": "6-12M",
            "capabilities": [
              "Autonomous Close & Insights with automated variance explanations",
              "AI reconciliation & exception detection",
              "Pre-close risk diagnostics"
            ]
          },
          "agent_mapping": {
            "primary_agents": ["Revenue Accountant Agent", "Revenue Narrator"],
            "supporting_agents": ["Data Management Agent", "Reconciliation AI", "DataFix AI"]
          }
        },
        {
          "id": "accounting_ledger",
          "name": "Accounting Ledger",
          "subtitle": "",
          "row": 2, "col": 6,
          "why_it_matters": "Controllers and CFOs need clean reconciliation from subledgers to ERP/GL, fast period close, and confidence in journal integrity.",
          "current_ai_capabilities": {
            "platform_features": [
              "Unified data warehouse (Billing, Revenue, Analytics, Benchmarks, CPQ)"
            ],
            "ai_agents": ["Reconciliation AI", "Revenue Accountant Agent", "Data Management Agent"],
            "mcp_tools": [
              "Access ledger-relevant objects (invoices, journal summaries, revenue schedules)",
              "Automated GL summary integrations"
            ]
          },
          "how_it_works_today": "Revenue and data agents assist with subledger-to-ERP/GL reconciliation, pointing out contracts/transactions causing deltas and drafting variance explanations.",
          "whats_coming": {
            "timeline": "6-12M",
            "capabilities": [
              "More automated journal workflows with pre-posting validation",
              "AI-first ledger narratives for board and auditors"
            ]
          },
          "agent_mapping": {
            "primary_agents": ["Reconciliation AI", "Revenue Accountant Agent"],
            "supporting_agents": ["Data Management Agent"]
          }
        },
        {
          "id": "usage_entitlement_enforcement",
          "name": "Usage and Entitlement Enforcement",
          "subtitle": "",
          "row": 3, "col": 6,
          "why_it_matters": "For usage-based models, over-consumption without enforcement causes revenue leakage. Over-enforcement hurts customer experience. Enforcement must be contract-aware.",
          "current_ai_capabilities": {
            "platform_features": [
              "Features & Entitlements in Monetization Catalog",
              "Usage anomaly detection"
            ],
            "ai_agents": ["Mediation/DACO Agents for usage anomalies"],
            "mcp_tools": [
              "Access usage, entitlements, subscription context",
              "Flag unexpected spikes or pattern violations"
            ]
          },
          "how_it_works_today": "Entitlement rules enforced through catalog + entitlements + mediation. Anomaly detection agents surface potential over/under-use.",
          "whats_coming": {
            "timeline": "6-12M",
            "capabilities": [
              "Dedicated usage/entitlement enforcement agents",
              "Trigger actions (notifications, plan changes, overages) via MCP",
              "Customer-visible transparency explaining entitlements and overages"
            ]
          },
          "agent_mapping": {
            "primary_agents": ["Mediation/DACO Agent"],
            "supporting_agents": ["DQ/Trino Agent", "Customer Portal Agent"]
          }
        },
        {
          "id": "reporting_dashboards",
          "name": "Reporting and Dashboards",
          "subtitle": "",
          "row": 4, "col": 6,
          "why_it_matters": "Many customers export to spreadsheets/BI, spend days on board decks, and struggle with real-time cross-product views. AI-ready reporting requires unified data.",
          "current_ai_capabilities": {
            "platform_features": [
              "Unified Data Platform consolidating Billing + Revenue + Analytics + Benchmarks + CPQ"
            ],
            "ai_agents": ["Query Assistant", "Revenue Narrator", "Revenue Manager Agent"],
            "mcp_tools": [
              "Natural language queries with auto-generated SQL",
              "Generate narrative explanations and forecasts"
            ]
          },
          "how_it_works_today": "Customers use unified reporting for cross-billing/revenue queries. AI-powered querying and narratives layer on top.",
          "whats_coming": {
            "timeline": "NOW-6M",
            "capabilities": [
              "Board decks generated via AI",
              "Real-time, conversational dashboards",
              "Role-aware, permission-aware data access for agents"
            ]
          },
          "agent_mapping": {
            "primary_agents": ["Query Assistant", "Revenue Manager Agent"],
            "supporting_agents": ["Revenue Narrator"]
          }
        },
        {
          "id": "tax",
          "name": "Tax",
          "subtitle": "",
          "row": 5, "col": 6,
          "why_it_matters": "Managing regional and global tax compliance across complex subscription structures is error-prone and audit-sensitive.",
          "current_ai_capabilities": {
            "platform_features": [
              "Tax engine integration",
              "Tax reporting as part of unified data"
            ],
            "ai_agents": ["Revenue agents and Data Management Agent for tax-related anomalies"],
            "mcp_tools": [
              "Access tax calculations and reporting",
              "Flag unusual effective tax rates"
            ]
          },
          "how_it_works_today": "Tax calculations handled by tax engine. Revenue agents can flag anomalies related to unusual tax outcomes.",
          "whats_coming": {
            "timeline": "12-24M",
            "capabilities": [
              "Tax-aware diagnostics and narratives",
              "Agents factoring tax into revenue forecasting and margin analysis"
            ]
          },
          "agent_mapping": {
            "primary_agents": ["Revenue Accountant Agent"],
            "supporting_agents": ["Data Management Agent"]
          }
        },
        {
          "id": "compliance",
          "name": "Compliance",
          "subtitle": "",
          "row": 6, "col": 6,
          "why_it_matters": "Compliance spans financial reporting (GAAP/IFRS), auditability, and operational incidents. AI must improve compliance, not undermine it.",
          "current_ai_capabilities": {
            "platform_features": [
              "Observability, explainability, auditability design principles",
              "Centralized logging, policy, and approvals via MCP + Anantha"
            ],
            "ai_agents": ["RCA Agent", "DQ/Trino Agent", "Data Management Agent"],
            "mcp_tools": [
              "Draft incident and compliance summaries",
              "Continuous data validation and audit readiness"
            ]
          },
          "how_it_works_today": "RCA Agent drafts incident RCAs. DQ/Trino provides diagnostics for compliance docs. Revenue agents generate explanations supporting audit.",
          "whats_coming": {
            "timeline": "6-12M",
            "capabilities": [
              "Agent-generated compliance packs (RCAs, reconciliations, validations, narratives)",
              "Unified audit/logging/observability for all agent decisions"
            ]
          },
          "agent_mapping": {
            "primary_agents": ["RCA Agent", "DQ/Trino Agent"],
            "supporting_agents": ["Data Management Agent", "Revenue Accountant Agent"]
          }
        }
      ]
    },
    // PHASE 7: LEARN
    {
      "id": "learn",
      "name": "Learn",
      "color": "#EF6C00",
      "agentic_goal": "Closed-loop intelligence",
      "strategy_context": "Turn raw monetization data into closed-loop intelligence that feeds back into Configure, Quote, Invoice, Collect, and Provision.",
      "capabilities": [
        {
          "id": "revenue_profit_insights",
          "name": "Revenue and Profit Insights",
          "subtitle": "",
          "row": 1, "col": 7,
          "why_it_matters": "Leaders need forward-looking, driver-based views of revenue, margin, and cash. Many rely on manual spreadsheets and siloed BI.",
          "current_ai_capabilities": {
            "platform_features": [
              "Unified Data Platform (Billing, Revenue, Analytics, Benchmarks, CPQ)",
              "Real-time billing forecasts with confidence ranges"
            ],
            "ai_agents": ["Revenue Accountant Agent", "Revenue Manager Agent", "Finance Intelligence agents"],
            "mcp_tools": [
              "Access subscriptions, invoices, revenue schedules, metrics",
              "Compute and explain revenue/profit KPIs"
            ]
          },
          "how_it_works_today": "Finance users or AI agents can ask for billing forecasts, margin by product, MRR trends and get numeric answers plus plain-language driver explanations.",
          "whats_coming": {
            "timeline": "6-12M",
            "capabilities": [
              "Autonomous close & insight loops",
              "Pre-close diagnostics and automated variance explanations",
              "Continuous profitability views across product/segment/channel"
            ]
          },
          "agent_mapping": {
            "primary_agents": ["Revenue Manager Agent", "Finance Intelligence Agent"],
            "supporting_agents": ["Revenue Accountant Agent"]
          }
        },
        {
          "id": "customer_insights",
          "name": "Customer Insights",
          "subtitle": "Churn Detect",
          "row": 2, "col": 7,
          "why_it_matters": "Retention is often more valuable than acquisition, but churn risk signals are spread across usage, billing, payments, support, and product.",
          "current_ai_capabilities": {
            "platform_features": [
              "Acquisition & Retention Knowledge Graph (ARK)",
              "Zephr AI Paywall for personalized offers"
            ],
            "ai_agents": ["Churn Agent", "Customer Health Agent"],
            "mcp_tools": [
              "Read usage, subscription events, collections data, entitlements",
              "Score churn risk and propose actions"
            ]
          },
          "how_it_works_today": "Churn/health agents use MCP to read context, score churn risk, and propose actions (offers via CPQ/paywall, CS outreach).",
          "whats_coming": {
            "timeline": "6-12M",
            "capabilities": [
              "Deeper lifecycle-aware churn models combining Quote, Invoice, Collect, Provision signals",
              "Automated 'next best action' offers",
              "Coordinated playbooks across CS, sales, marketing"
            ]
          },
          "agent_mapping": {
            "primary_agents": ["Churn Agent", "Customer Health Agent"],
            "supporting_agents": ["Collections Manager Agent", "Customer Success Agent"]
          }
        },
        {
          "id": "offer_insights",
          "name": "Offer Insights",
          "subtitle": "",
          "row": 3, "col": 7,
          "why_it_matters": "Businesses struggle to understand which offers, bundles, and discounts actually drive profitable, durable growth.",
          "current_ai_capabilities": {
            "platform_features": [
              "Rateplan & SKU Insights (product performance, pricing elasticity)",
              "Intelligent Merchandising and Promotions Management"
            ],
            "ai_agents": ["Outcomes Simulation Agent"],
            "mcp_tools": [
              "Measure offer/deal performance on ARR, margin, churn, adoption",
              "Feed insights back into pricing and catalog decisions"
            ]
          },
          "how_it_works_today": "Using MCP + data platform, agents measure offer performance versus peers and feed back into pricing/catalog decisions or CPQ guidance.",
          "whats_coming": {
            "timeline": "6-12M",
            "capabilities": [
              "Closed-loop experimentation framework",
              "AI-driven analysis of which deals to scale up or retire",
              "Direct feeding into catalog and CPQ rules"
            ]
          },
          "agent_mapping": {
            "primary_agents": ["Outcomes Simulation Agent"],
            "supporting_agents": ["Developer MCP"]
          }
        },
        {
          "id": "customer_value_intelligence",
          "name": "Customer Value Intelligence",
          "subtitle": "Transactions, Usage, Risk",
          "row": 4, "col": 7,
          "why_it_matters": "Decisions about upsell, retention, or pricing should be based on true customer value: past transactions, current usage, credit and churn risk. Without unified view, teams optimize on wrong signals.",
          "current_ai_capabilities": {
            "platform_features": [
              "Unified monetization data platform",
              "ARK (Acquisition & Retention Knowledge Graph)"
            ],
            "ai_agents": ["Churn Agent", "Collections Agent", "Revenue Agents", "Quote Agent", "Customer Health Agent"],
            "mcp_tools": [
              "Share context across agents via MCP and unified data",
              "Enable quoting guided by account-level value metrics"
            ]
          },
          "how_it_works_today": "CVI is emerging as a cross-agent concept. Agents share context via MCP enabling richer insights.",
          "whats_coming": {
            "timeline": "12-24M",
            "capabilities": [
              "First-class CVI dashboards and agents",
              "Surfacing LTV, NRR, risk-adjusted value, product coverage, whitespace",
              "Recommended actions per customer"
            ]
          },
          "agent_mapping": {
            "primary_agents": ["Customer Health Agent"],
            "supporting_agents": ["Churn Agent", "Collections Manager Agent", "Quote Agent"]
          }
        },
        {
          "id": "price_profit_optimization",
          "name": "Price/Profit Optimization",
          "subtitle": "",
          "row": 5, "col": 7,
          "why_it_matters": "Pricing teams must navigate usage models, dynamic pricing, discounts, and commitments while balancing growth vs margin vs churn. Manual price studies can't keep up.",
          "current_ai_capabilities": {
            "platform_features": [
              "Dynamic Pricing using real-time customer and business context",
              "Rateplan & SKU Insights for elasticity analysis"
            ],
            "ai_agents": ["Outcomes Simulation Agent"],
            "mcp_tools": [
              "Simulate what-if plan and pricing scenarios",
              "Revenue and margin projections"
            ]
          },
          "how_it_works_today": "Pricing teams use simulation and insights to test new price points and understand profitability impacts before changes go live.",
          "whats_coming": {
            "timeline": "12-24M",
            "capabilities": [
              "Automated optimization loops",
              "Agents continuously suggesting or applying pricing adjustments to hit goals"
            ]
          },
          "agent_mapping": {
            "primary_agents": ["Outcomes Simulation Agent"],
            "supporting_agents": ["Developer MCP", "Revenue Manager Agent"]
          }
        },
        {
          "id": "partner_channel_intelligence",
          "name": "Partner/Channel Intelligence",
          "subtitle": "",
          "row": 6, "col": 7,
          "why_it_matters": "Partner and channel motions are critical for scale, but performance data is siloed and incentives/settlements lack ROI metrics.",
          "current_ai_capabilities": {
            "platform_features": [
              "Business Context Service + Commerce Foundation with channel context",
              "Unified data platform with CPQ, Billing, Revenue, Collections"
            ],
            "ai_agents": ["Collections & Revenue agents with account structure analysis"],
            "mcp_tools": [
              "Analyze channel/partner revenue and margin",
              "Track churn and expansion by channel"
            ]
          },
          "how_it_works_today": "Channel intelligence is mostly reporting-driven using unified data and context attributes. AI starting to layer narratives and anomaly detection.",
          "whats_coming": {
            "timeline": "12-24M",
            "capabilities": [
              "Dedicated partner/channel intelligence agents",
              "Track partner performance vs targets",
              "Recommend adjustments to incentives and channel mix"
            ]
          },
          "agent_mapping": {
            "primary_agents": ["Revenue Manager Agent"],
            "supporting_agents": ["Collections Manager Agent"]
          }
        },
        {
          "id": "benchmarks",
          "name": "Benchmarks",
          "subtitle": "",
          "row": 7, "col": 7,
          "why_it_matters": "Execs want to know if they're doing well for their segment and where they under/over-perform vs peers.",
          "current_ai_capabilities": {
            "platform_features": [
              "Unified data warehouse planned to incorporate benchmarks",
              "Anonymized industry benchmarks in Rateplan & SKU Insights"
            ],
            "ai_agents": ["Revenue agents with benchmark awareness"],
            "mcp_tools": [
              "Access benchmark data for comparison",
              "Incorporate peer comparison into recommendations"
            ]
          },
          "how_it_works_today": "Early stages. Benchmarks mainly conceptual and pilot-level, used in pricing/offer analysis.",
          "whats_coming": {
            "timeline": "12-24M",
            "capabilities": [
              "Benchmark-aware agents and dashboards",
              "Compare growth, churn, pricing, margins vs anonymized peers",
              "Recommend focus areas based on peer comparison"
            ]
          },
          "agent_mapping": {
            "primary_agents": ["Revenue Manager Agent"],
            "supporting_agents": ["Outcomes Simulation Agent"]
          }
        }
      ]
    },
    // PHASE 8: SUSTAIN AND GROW
    {
      "id": "sustain_grow",
      "name": "Sustain and Grow",
      "color": "#1976D2",
      "agentic_goal": "Proactive retention & expansion",
      "strategy_context": "As growth matures, net retention depends on identifying at-risk customers early and deploying targeted, profitable win-back offers and expansion paths.",
      "capabilities": [
        {
          "id": "churn_prevent",
          "name": "Churn Prevention",
          "subtitle": "Win-back Offers",
          "row": 1, "col": 8,
          "why_it_matters": "Net retention depends on identifying at-risk customers early and deploying targeted, profitable win-back offers—not blanket discounts.",
          "current_ai_capabilities": {
            "platform_features": [
              "Zephr AI Paywall for real-time offer personalization (78% LTV lift example)",
              "Collections AI connecting billing + CRM + support for churn risk"
            ],
            "ai_agents": ["Churn Agent", "Customer Health Agent"],
            "mcp_tools": [
              "Read usage, billing, collections, entitlements",
              "Compute risk and invoke win-back offers in CPQ/paywalls"
            ]
          },
          "how_it_works_today": "Early implementations use churn/health scoring plus AI-driven offers via Zephr AI Paywall to identify at-risk segments and present retention offers.",
          "whats_coming": {
            "timeline": "6-12M",
            "capabilities": [
              "Closed-loop churn prevention tying together Churn + Health + CPQ + Collections + CS",
              "Agents selecting and deploying right win-back playbook per customer",
              "Clear measurement of retention and profitability"
            ]
          },
          "agent_mapping": {
            "primary_agents": ["Churn Agent", "Customer Health Agent"],
            "supporting_agents": ["Collections Manager Agent", "Quote Agent"]
          }
        },
        {
          "id": "renewals",
          "name": "Renewals",
          "subtitle": "CPQ, Upsell/Cross-sell",
          "row": 2, "col": 8,
          "why_it_matters": "Renewal moments are the best point for expansion (upsell, cross-sell) and a major churn risk if manual, late, or mis-priced.",
          "current_ai_capabilities": {
            "platform_features": [
              "CPQ combining new sales, amendments, renewals in single quote",
              "Auto-gen Renewal Quotes from contract state and usage history",
              "Guided selling and dynamic pricing in CPQ"
            ],
            "ai_agents": ["Quote Agent / Deal Assist", "Deal Sense agents"],
            "mcp_tools": [
              "Read current subscriptions and contracts",
              "Generate proposed renewal quotes with upsells/cross-sells",
              "Push into CPQ for approval"
            ]
          },
          "how_it_works_today": "AI-assisted renewals use account insights + contract history to auto-generate renewal quotes, propose expansion paths, let reps compare alternatives in CPQ.",
          "whats_coming": {
            "timeline": "6-12M",
            "capabilities": [
              "Fully agentic renewal flows for B2B (agents watching renewal horizons, pre-staging quotes)",
              "Integration with AI Paywall & Customer Health for B2C/hybrid",
              "Coordinated self-serve and assisted renewal for high-value accounts"
            ]
          },
          "agent_mapping": {
            "primary_agents": ["Quote Agent / Deal Assist"],
            "supporting_agents": ["Customer Health Agent", "Revenue Manager Agent"]
          }
        },
        {
          "id": "customer_success",
          "name": "Customer Success",
          "subtitle": "Health, Education",
          "row": 3, "col": 8,
          "why_it_matters": "CS teams must monitor health signals, drive adoption and expansion, and educate at scale. Manual processes don't scale.",
          "current_ai_capabilities": {
            "platform_features": [
              "Unified Data Platform for single view of Commerce + Billing + AR + Revenue"
            ],
            "ai_agents": ["Customer Success Agent", "Customer Health Agent", "Zuora AI Help"],
            "mcp_tools": [
              "Access subscriptions, invoices, usage, revenue, collections, entitlements",
              "Compute health scores and generate recommended plays"
            ]
          },
          "how_it_works_today": "CS teams use reporting + early health/churn agents for account metrics and narratives. Zuora AI Help provides education layer for product and billing concepts.",
          "whats_coming": {
            "timeline": "6-12M",
            "capabilities": [
              "End-to-end CS playbooks (education campaigns, success plans, EBR prep, renewal prep)",
              "Proactive education & in-product guidance",
              "Context-aware help driven by actual contract and usage context"
            ]
          },
          "agent_mapping": {
            "primary_agents": ["Customer Success Agent", "Customer Health Agent"],
            "supporting_agents": ["Zuora AI Help", "Anantha Concierge"]
          }
        }
      ]
    }
  ]
}
```

---

## 5. IMAGE PROCESSING MODULE

### 5.1 Requirements

The app must extract I/R scores from an uploaded image of the completed assessment.

### 5.2 Implementation Approach

**Option A: Claude Vision API (Recommended)**
Use Anthropic's Claude API with vision capabilities to analyze the image and extract scores.

```python
import anthropic
import base64

def extract_scores_from_image(image_path: str) -> dict:
    """
    Use Claude Vision to extract I/R scores from assessment image.
    Returns dict mapping capability_id to {importance: int, readiness: int}
    """
    client = anthropic.Anthropic()
    
    with open(image_path, "rb") as f:
        image_data = base64.standard_b64encode(f.read()).decode("utf-8")
    
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": image_data
                        }
                    },
                    {
                        "type": "text",
                        "text": EXTRACTION_PROMPT
                    }
                ]
            }
        ]
    )
    
    return parse_extraction_response(message.content[0].text)
```

### 5.3 Extraction Prompt

```python
EXTRACTION_PROMPT = """
Analyze this Recurring Revenue Management Lifecycle Assessment image and extract all Importance (I) and Readiness (R) scores.

The assessment has 8 phases (columns) and up to 7 capability rows per phase:
1. Configure and Price
2. Quote and Sell
3. Invoice
4. Collect
5. Provision
6. Recognize and Report
7. Learn
8. Sustain and Grow

For each capability card, extract:
- Capability name
- I score (Importance, 1-10)
- R score (Readiness, 1-10)

Return as JSON in this exact format:
{
  "scores": [
    {
      "phase": "Configure and Price",
      "capability": "Offer/Catalog Management",
      "importance": 8,
      "readiness": 4
    },
    ...
  ],
  "extraction_confidence": "high|medium|low",
  "notes": "Any issues or unclear readings"
}

If a score is illegible or missing, use null.
If a cell is empty (marked with dash), skip it.
"""
```

### 5.4 Score Validation

```python
def validate_scores(extracted_scores: dict) -> tuple[dict, list]:
    """
    Validate extracted scores and return cleaned data + warnings.
    """
    warnings = []
    validated = []
    
    for score in extracted_scores.get("scores", []):
        # Validate score ranges
        imp = score.get("importance")
        rdy = score.get("readiness")
        
        if imp is not None and not (1 <= imp <= 10):
            warnings.append(f"{score['capability']}: Invalid importance score {imp}")
            imp = max(1, min(10, imp))  # Clamp
            
        if rdy is not None and not (1 <= rdy <= 10):
            warnings.append(f"{score['capability']}: Invalid readiness score {rdy}")
            rdy = max(1, min(10, rdy))
            
        validated.append({
            **score,
            "importance": imp,
            "readiness": rdy
        })
    
    return {"scores": validated}, warnings
```

---

## 6. PRIORITY ANALYSIS ENGINE

### 6.1 Priority Categories

```python
def categorize_priority(importance: int, readiness: int) -> str:
    """
    Categorize based on I/R matrix:
    - URGENT_GAP: High I (>=7) + Low R (<=4) 
    - CRITICAL_GAP: High I (>=7) + Medium R (5-6)
    - STRENGTH: High I (>=7) + High R (>=7)
    - OPPORTUNITY: Medium I (4-6) + Low R (<=4)
    - MAINTAIN: Medium I (4-6) + High R (>=7)
    - DEPRIORITIZE: Low I (<=3)
    """
    if importance <= 3:
        return "DEPRIORITIZE"
    elif importance >= 7:
        if readiness <= 4:
            return "URGENT_GAP"
        elif readiness <= 6:
            return "CRITICAL_GAP"
        else:
            return "STRENGTH"
    else:  # Medium importance (4-6)
        if readiness <= 4:
            return "OPPORTUNITY"
        else:
            return "MAINTAIN"
```

### 6.2 Gap Score Calculation

```python
def calculate_gap_score(importance: int, readiness: int) -> float:
    """
    Calculate gap score for prioritization.
    Higher score = more urgent.
    Formula: importance * (10 - readiness) / 10
    """
    return importance * (10 - readiness) / 10
```

### 6.3 Timeline Mapping

```python
TIMELINE_MAPPING = {
    "URGENT_GAP": {
        "horizon": "NOW (0-6 months)",
        "agent_tier": "Developer Agents + Quick Wins",
        "investment": "HIGH"
    },
    "CRITICAL_GAP": {
        "horizon": "NEAR (6-12 months)",
        "agent_tier": "Diagnostic Agents",
        "investment": "MEDIUM-HIGH"
    },
    "STRENGTH": {
        "horizon": "PROTECT",
        "agent_tier": "Monitor + Enhance",
        "investment": "MAINTAIN"
    },
    "OPPORTUNITY": {
        "horizon": "LATER (12-24 months)",
        "agent_tier": "Orchestration Agents",
        "investment": "MEDIUM"
    },
    "MAINTAIN": {
        "horizon": "AS NEEDED",
        "agent_tier": "Standard Operations",
        "investment": "LOW"
    },
    "DEPRIORITIZE": {
        "horizon": "BACKLOG",
        "agent_tier": "N/A",
        "investment": "MINIMAL"
    }
}
```

---

## 7. REPORT GENERATION

### 7.1 Report Structure

```python
REPORT_SECTIONS = [
    "executive_summary",
    "priority_matrix_visual",
    "urgent_gaps_detail",
    "strength_protection",
    "phase_by_phase_analysis",
    "agent_roadmap",
    "mcp_integration_plan",
    "implementation_timeline",
    "next_steps"
]
```

### 7.2 Report Generation with LLM

```python
def generate_strategic_report(
    scores: dict,
    knowledge_base: dict,
    customer_context: dict = None
) -> str:
    """
    Generate comprehensive strategic report using Claude.
    """
    client = anthropic.Anthropic()
    
    # Prepare analysis data
    analyzed_capabilities = analyze_all_capabilities(scores, knowledge_base)
    priority_summary = create_priority_summary(analyzed_capabilities)
    
    prompt = f"""
    You are a strategic product consultant specializing in Order-to-Cash transformation and AI/MCP readiness.
    
    Based on the following assessment results and knowledge base, generate a comprehensive 
    Strategic Priority Guide for AI Agent and MCP adoption.
    
    ## Assessment Results
    {json.dumps(priority_summary, indent=2)}
    
    ## Knowledge Base Context
    {json.dumps(knowledge_base['mcp_overview'], indent=2)}
    {json.dumps(knowledge_base['agent_inventory'], indent=2)}
    
    ## Analyzed Capabilities (with agent mappings)
    {json.dumps(analyzed_capabilities, indent=2)}
    
    ## Customer Context (if provided)
    {json.dumps(customer_context or {}, indent=2)}
    
    Generate a strategic report with these sections:
    
    1. **Executive Summary** (2-3 paragraphs)
       - Overall readiness assessment
       - Top 3 urgent priorities
       - Key strengths to protect
    
    2. **Priority Matrix Analysis**
       - Count by category (Urgent Gap, Critical Gap, Strength, etc.)
       - Phase-level patterns
    
    3. **Urgent Gaps (High I + Low R) - Detailed Analysis**
       For each urgent gap:
       - Capability name and phase
       - Why it matters (from knowledge base)
       - Current AI/MCP capabilities available TODAY
       - Recommended agents to deploy
       - Quick wins vs. longer-term initiatives
    
    4. **Strengths to Protect (High I + High R)**
       - What's working
       - How to maintain competitive advantage
       - Agents/MCP tools that can enhance
    
    5. **Phase-by-Phase Recommendations**
       For each of the 8 phases:
       - Overall phase health score
       - Key gaps and strengths
       - Recommended focus areas
    
    6. **AI Agent Roadmap**
       - NOW (0-6 months): Which agents to enable immediately
       - NEAR (6-12 months): Diagnostic and integration agents
       - LATER (12-24 months): Orchestration and autonomous agents
    
    7. **MCP Integration Plan**
       - Developer MCP quick wins
       - Remote MCP Server timeline
       - MCP Gateway opportunities
    
    8. **Implementation Timeline**
       - 30/60/90 day plan
       - Key milestones
       - Dependencies
    
    9. **Next Steps**
       - Immediate actions
       - Stakeholder alignment needed
       - Success metrics
    
    Format the report in clean Markdown suitable for conversion to DOCX.
    Use tables where appropriate.
    Include specific agent names and MCP tools from the knowledge base.
    Be actionable and specific, not generic.
    """
    
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=8192,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return message.content[0].text
```

---

## 8. STREAMLIT APPLICATION

### 8.1 File Structure

```
o2c_assessment_app/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── config.py                   # Configuration settings
├── knowledge_base.json         # Complete capability knowledge base
├── modules/
│   ├── __init__.py
│   ├── image_processor.py      # Image upload and score extraction
│   ├── score_analyzer.py       # Priority analysis engine
│   ├── report_generator.py     # Report generation with LLM
│   └── export_handler.py       # DOCX/PDF export
├── templates/
│   ├── report_template.docx    # Word template for export
│   └── styles.css              # Custom Streamlit styling
├── assets/
│   └── lifecycle_assessment.html  # Reference assessment template
└── tests/
    ├── test_extraction.py
    ├── test_analysis.py
    └── sample_images/
```

### 8.2 Main Application (app.py)

```python
import streamlit as st
import json
from pathlib import Path

from modules.image_processor import extract_scores_from_image
from modules.score_analyzer import analyze_capabilities, create_priority_matrix
from modules.report_generator import generate_strategic_report
from modules.export_handler import export_to_docx, export_to_pdf

# Page config
st.set_page_config(
    page_title="O2C AI Readiness Assessment",
    page_icon="🎯",
    layout="wide"
)

# Load knowledge base
@st.cache_data
def load_knowledge_base():
    with open("knowledge_base.json") as f:
        return json.load(f)

kb = load_knowledge_base()

# Header
st.title("🎯 O2C AI Agent & MCP Readiness Assessment")
st.markdown("""
Upload your completed Lifecycle Assessment to generate a strategic priority guide 
for AI Agent and MCP adoption across your Order-to-Cash ecosystem.
""")

# Sidebar for context
with st.sidebar:
    st.header("Assessment Context")
    company_name = st.text_input("Company/Customer Name", "")
    industry = st.selectbox("Industry", [
        "Technology/SaaS",
        "Media & Publishing",
        "Telecommunications",
        "Manufacturing",
        "Healthcare",
        "Financial Services",
        "Other"
    ])
    primary_model = st.selectbox("Primary Business Model", [
        "Pure Subscription",
        "Usage-Based",
        "Hybrid (Subscription + Usage)",
        "Transactional + Recurring"
    ])
    
    st.divider()
    st.header("Analysis Options")
    include_agent_details = st.checkbox("Include detailed agent descriptions", True)
    include_mcp_roadmap = st.checkbox("Include MCP integration roadmap", True)
    focus_areas = st.multiselect(
        "Priority Focus Areas",
        ["Billing Operations", "Revenue Recognition", "Collections", "Customer Success", "Pricing"],
        default=[]
    )

# Main content
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📤 Upload Assessment")
    uploaded_file = st.file_uploader(
        "Upload completed assessment image",
        type=["png", "jpg", "jpeg", "pdf"],
        help="Upload a photo or scan of your completed Lifecycle Assessment with I/R scores filled in"
    )
    
    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Assessment", use_column_width=True)

with col2:
    st.header("📊 Extraction Preview")
    
    if uploaded_file:
        with st.spinner("Extracting scores using AI vision..."):
            # Save uploaded file temporarily
            temp_path = Path(f"/tmp/{uploaded_file.name}")
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getvalue())
            
            # Extract scores
            extracted_data, warnings = extract_scores_from_image(str(temp_path))
            
            if warnings:
                st.warning("⚠️ Extraction warnings:")
                for w in warnings:
                    st.write(f"- {w}")
            
            st.success(f"✅ Extracted {len(extracted_data['scores'])} capability scores")
            
            # Show editable preview
            st.subheader("Review & Edit Scores")
            edited_scores = []
            
            for phase in kb['phases']:
                with st.expander(f"📁 {phase['name']}", expanded=False):
                    for cap in phase['capabilities']:
                        # Find extracted score for this capability
                        extracted = next(
                            (s for s in extracted_data['scores'] 
                             if s['capability'].lower() in cap['name'].lower()),
                            {"importance": None, "readiness": None}
                        )
                        
                        cols = st.columns([3, 1, 1])
                        with cols[0]:
                            st.write(cap['name'])
                        with cols[1]:
                            imp = st.number_input(
                                "I", 
                                min_value=1, max_value=10,
                                value=extracted['importance'] or 5,
                                key=f"i_{cap['id']}"
                            )
                        with cols[2]:
                            rdy = st.number_input(
                                "R",
                                min_value=1, max_value=10,
                                value=extracted['readiness'] or 5,
                                key=f"r_{cap['id']}"
                            )
                        
                        edited_scores.append({
                            "capability_id": cap['id'],
                            "phase_id": phase['id'],
                            "importance": imp,
                            "readiness": rdy
                        })

# Analysis and Report Generation
st.divider()

if uploaded_file and st.button("🚀 Generate Strategic Report", type="primary"):
    
    # Prepare customer context
    customer_context = {
        "company": company_name,
        "industry": industry,
        "business_model": primary_model,
        "focus_areas": focus_areas
    }
    
    with st.spinner("Analyzing capabilities and generating report..."):
        # Analyze
        analysis = analyze_capabilities(edited_scores, kb)
        priority_matrix = create_priority_matrix(analysis)
        
        # Generate report
        report_md = generate_strategic_report(
            scores={"scores": edited_scores},
            knowledge_base=kb,
            customer_context=customer_context
        )
        
        # Store in session state
        st.session_state['report'] = report_md
        st.session_state['analysis'] = analysis
        st.session_state['priority_matrix'] = priority_matrix
    
    st.success("✅ Report generated!")

# Display Report
if 'report' in st.session_state:
    st.header("📋 Strategic Priority Guide")
    
    # Priority Matrix Visualization
    with st.expander("🎯 Priority Matrix Overview", expanded=True):
        pm = st.session_state['priority_matrix']
        
        cols = st.columns(6)
        categories = ["URGENT_GAP", "CRITICAL_GAP", "STRENGTH", "OPPORTUNITY", "MAINTAIN", "DEPRIORITIZE"]
        colors = ["🔴", "🟠", "🟢", "🟡", "🔵", "⚪"]
        
        for i, (cat, color) in enumerate(zip(categories, colors)):
            with cols[i]:
                count = pm.get(cat, 0)
                st.metric(cat.replace("_", " ").title(), f"{color} {count}")
    
    # Full Report
    st.markdown(st.session_state['report'])
    
    # Export Options
    st.divider()
    st.header("📥 Export Report")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Download as DOCX"):
            docx_bytes = export_to_docx(st.session_state['report'], customer_context)
            st.download_button(
                label="Download DOCX",
                data=docx_bytes,
                file_name=f"O2C_Assessment_{company_name or 'Report'}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
    
    with col2:
        if st.button("📑 Download as PDF"):
            pdf_bytes = export_to_pdf(st.session_state['report'], customer_context)
            st.download_button(
                label="Download PDF",
                data=pdf_bytes,
                file_name=f"O2C_Assessment_{company_name or 'Report'}.pdf",
                mime="application/pdf"
            )
    
    with col3:
        if st.button("📝 Download as Markdown"):
            st.download_button(
                label="Download MD",
                data=st.session_state['report'],
                file_name=f"O2C_Assessment_{company_name or 'Report'}.md",
                mime="text/markdown"
            )
```

### 8.3 Requirements

```txt
# requirements.txt
streamlit>=1.30.0
anthropic>=0.18.0
python-docx>=1.1.0
markdown>=3.5.0
Pillow>=10.0.0
pandas>=2.0.0
plotly>=5.18.0
weasyprint>=60.0  # For PDF generation
pydantic>=2.0.0
python-dotenv>=1.0.0
```

---

## 9. CLI BUILD INSTRUCTIONS

### 9.1 Setup Commands

```bash
# Create project directory
mkdir o2c_assessment_app
cd o2c_assessment_app

# Initialize Python environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
echo "ANTHROPIC_API_KEY=your_key_here" > .env

# Create directory structure
mkdir -p modules templates assets tests/sample_images
```

### 9.2 Build Order

1. Create `knowledge_base.json` with full capability data
2. Implement `modules/image_processor.py`
3. Implement `modules/score_analyzer.py`
4. Implement `modules/report_generator.py`
5. Implement `modules/export_handler.py`
6. Create `app.py` main application
7. Test with sample images
8. Deploy to Streamlit Cloud or container

### 9.3 Testing

```bash
# Run tests
pytest tests/

# Run app locally
streamlit run app.py

# Build Docker container
docker build -t o2c-assessment .
docker run -p 8501:8501 o2c-assessment
```

---

## 10. CONFIGURATION

### 10.1 config.py

```python
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# API Configuration
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
CLAUDE_MODEL = "claude-sonnet-4-20250514"

# File Paths
BASE_DIR = Path(__file__).parent
KNOWLEDGE_BASE_PATH = BASE_DIR / "knowledge_base.json"
TEMPLATE_DIR = BASE_DIR / "templates"

# Analysis Thresholds
IMPORTANCE_HIGH_THRESHOLD = 7
IMPORTANCE_LOW_THRESHOLD = 3
READINESS_HIGH_THRESHOLD = 7
READINESS_LOW_THRESHOLD = 4

# Report Configuration
MAX_REPORT_LENGTH = 12000
INCLUDE_TECHNICAL_DETAILS = True
```

---

## 11. DEPLOYMENT

### 11.1 Streamlit Cloud

1. Push code to GitHub
2. Connect to Streamlit Cloud
3. Set `ANTHROPIC_API_KEY` in Streamlit secrets
4. Deploy

### 11.2 Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

---

## 12. SUCCESS CRITERIA

1. **Image Processing**: Successfully extract 80%+ of scores from typical assessment images
2. **Analysis Accuracy**: Correctly categorize all capabilities into priority buckets
3. **Report Quality**: Generate actionable, specific recommendations using knowledge base
4. **Export Functionality**: Clean DOCX/PDF output suitable for executive presentation
5. **Performance**: Complete analysis in under 60 seconds

---

## 13. FUTURE ENHANCEMENTS

1. **Interactive Assessment**: Digital form instead of image upload
2. **Multi-assessment Comparison**: Track progress over time
3. **Benchmarking**: Compare against anonymized industry peers
4. **Integration**: Connect to Zuora sandbox for live capability validation
5. **Collaboration**: Multi-user assessment with role-based input

---

*Specification Version 1.0 | January 2025*
