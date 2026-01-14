# grid_layout.py
# Exact grid mapping for the O2C Lifecycle Assessment
# 8 columns (phases) × 7 rows

# Full descriptions for each capability (used as subtitles)
CAPABILITY_DESCRIPTIONS = {
    # Configure and Price
    "offer_catalog_management": "Managing price, usage, and promotions.",
    "price_management": "Standardizing pricing structures.",
    "revenue_planning": "Projecting future financial performance.",
    "incentive_management": "Handling rebates and discounts.",
    "channel_management": "Managing indirect sales routes.",

    # Quote and Sell
    "opportunity_capture": "Integrating eCommerce, CRM, and partner data.",
    "customer_partner_portals": "Self-service interfaces.",
    "guided_selling": "Utilizing CPQ and price guidance.",
    "customer_risk_fraud": "Assessing buyer legitimacy.",
    "contract_management": "Managing legal agreements.",
    "inventory_ship_availability": "Real-time product tracking.",

    # Invoice
    "order_management": "Processing incoming customer requests.",
    "billing_invoice": "Generating and sending customer bills.",
    "rating_charging": "Calculating costs based on usage.",
    "usage_data_mediation": "Aggregating data for billing.",
    "anomaly_detection": "Identifying outliers in billing data.",
    "dispute_prediction": "Identifying likely billing conflicts before they occur.",

    # Collect
    "payment_routing": "Handling transaction flows.",
    "customer_credit_management": "Monitoring creditworthiness.",
    "dunning_payment_retry": "Managing failed payments.",
    "collections": "Recovering outstanding debts.",
    "partner_settlement": "Managing incentives and payments for partners.",

    # Provision
    "entitlement_management": "Defining what a customer is allowed to access.",
    "inventory": "Tracking physical or digital stock.",
    "fulfillment_ship": "Executing product delivery.",
    "deployment_provisioning": "Activating services for the user.",

    # Recognize and Report
    "revenue_recognition": "Aligning income with accounting standards.",
    "accounting_ledger": "Maintaining financial records.",
    "usage_entitlement_enforcement": "Ensuring users stay within contracted limits.",
    "reporting_dashboards": "Visualizing business performance.",
    "tax": "Managing regional and global tax compliance.",
    "compliance": "Adhering to regulatory requirements.",

    # Learn
    "revenue_profit_insights": "Analyzing financial health.",
    "customer_insights": "Detecting churn signals.",
    "offer_insights": "Evaluating the performance of specific deals.",
    "customer_value_intelligence": "Blending transaction, usage, and risk data.",
    "price_profit_optimization": "Refining pricing for better margins.",
    "partner_channel_intelligence": "Monitoring partner performance.",
    "benchmarks": "Comparing performance against industry standards.",

    # Sustain and Grow
    "churn_prevent": "Deploying win-back offers.",
    "renewals": "Managing CPQ for upsells and cross-sells.",
    "customer_success": "Monitoring health and providing education.",
}

PHASES = [
    {"id": "configure_price", "name": "Configure\nand Price", "color": "#2E7D32", "text_color": "white", "col": 0},
    {"id": "quote_sell", "name": "Quote and\nSell", "color": "#1565C0", "text_color": "white", "col": 1},
    {"id": "invoice", "name": "Invoice", "color": "#7B1FA2", "text_color": "white", "col": 2},
    {"id": "collect", "name": "Collect", "color": "#00838F", "text_color": "white", "col": 3},
    {"id": "provision", "name": "Provision", "color": "#F9A825", "text_color": "#333333", "col": 4},
    {"id": "recognize_report", "name": "Recognize\nand Report", "color": "#6A1B9A", "text_color": "white", "col": 5},
    {"id": "learn", "name": "Learn", "color": "#EF6C00", "text_color": "white", "col": 6},
    {"id": "sustain_grow", "name": "Sustain\nand Grow", "color": "#1976D2", "text_color": "white", "col": 7},
]

# Grid layout: 7 rows × 8 columns
# Each cell is either a capability dict or None (empty cell)
GRID_LAYOUT = [
    # Row 0 (Row 1 in visual)
    [
        {"id": "offer_catalog_management", "name": "Offer/Catalog Management", "subtitle": CAPABILITY_DESCRIPTIONS["offer_catalog_management"], "phase_id": "configure_price"},
        {"id": "opportunity_capture", "name": "Opportunity Capture", "subtitle": CAPABILITY_DESCRIPTIONS["opportunity_capture"], "phase_id": "quote_sell"},
        {"id": "order_management", "name": "Order Management", "subtitle": CAPABILITY_DESCRIPTIONS["order_management"], "phase_id": "invoice"},
        {"id": "payment_routing", "name": "Payment and Routing", "subtitle": CAPABILITY_DESCRIPTIONS["payment_routing"], "phase_id": "collect"},
        {"id": "entitlement_management", "name": "Entitlement Management", "subtitle": CAPABILITY_DESCRIPTIONS["entitlement_management"], "phase_id": "provision"},
        {"id": "revenue_recognition", "name": "Revenue Recognition", "subtitle": CAPABILITY_DESCRIPTIONS["revenue_recognition"], "phase_id": "recognize_report"},
        {"id": "revenue_profit_insights", "name": "Revenue and Profit Insights", "subtitle": CAPABILITY_DESCRIPTIONS["revenue_profit_insights"], "phase_id": "learn"},
        {"id": "churn_prevent", "name": "Churn Prevention", "subtitle": CAPABILITY_DESCRIPTIONS["churn_prevent"], "phase_id": "sustain_grow"},
    ],
    # Row 1 (Row 2 in visual)
    [
        {"id": "price_management", "name": "Price Management", "subtitle": CAPABILITY_DESCRIPTIONS["price_management"], "phase_id": "configure_price"},
        {"id": "customer_partner_portals", "name": "Customer and Partner Portals", "subtitle": CAPABILITY_DESCRIPTIONS["customer_partner_portals"], "phase_id": "quote_sell"},
        {"id": "billing_invoice", "name": "Billing, Invoice", "subtitle": CAPABILITY_DESCRIPTIONS["billing_invoice"], "phase_id": "invoice"},
        {"id": "customer_credit_management", "name": "Customer Credit Management", "subtitle": CAPABILITY_DESCRIPTIONS["customer_credit_management"], "phase_id": "collect"},
        {"id": "inventory", "name": "Inventory", "subtitle": CAPABILITY_DESCRIPTIONS["inventory"], "phase_id": "provision"},
        {"id": "accounting_ledger", "name": "Accounting Ledger", "subtitle": CAPABILITY_DESCRIPTIONS["accounting_ledger"], "phase_id": "recognize_report"},
        {"id": "customer_insights", "name": "Customer Insights", "subtitle": CAPABILITY_DESCRIPTIONS["customer_insights"], "phase_id": "learn"},
        {"id": "renewals", "name": "Renewals", "subtitle": CAPABILITY_DESCRIPTIONS["renewals"], "phase_id": "sustain_grow"},
    ],
    # Row 2 (Row 3 in visual)
    [
        {"id": "revenue_planning", "name": "Revenue Planning", "subtitle": CAPABILITY_DESCRIPTIONS["revenue_planning"], "phase_id": "configure_price"},
        {"id": "guided_selling", "name": "Guided Selling", "subtitle": CAPABILITY_DESCRIPTIONS["guided_selling"], "phase_id": "quote_sell"},
        {"id": "rating_charging", "name": "Rating and Charging", "subtitle": CAPABILITY_DESCRIPTIONS["rating_charging"], "phase_id": "invoice"},
        {"id": "dunning_payment_retry", "name": "Dunning and Payment Retry", "subtitle": CAPABILITY_DESCRIPTIONS["dunning_payment_retry"], "phase_id": "collect"},
        {"id": "fulfillment_ship", "name": "Fulfillment and Ship", "subtitle": CAPABILITY_DESCRIPTIONS["fulfillment_ship"], "phase_id": "provision"},
        {"id": "usage_entitlement_enforcement", "name": "Usage and Entitlement Enforcement", "subtitle": CAPABILITY_DESCRIPTIONS["usage_entitlement_enforcement"], "phase_id": "recognize_report"},
        {"id": "offer_insights", "name": "Offer Insights", "subtitle": CAPABILITY_DESCRIPTIONS["offer_insights"], "phase_id": "learn"},
        {"id": "customer_success", "name": "Customer Success", "subtitle": CAPABILITY_DESCRIPTIONS["customer_success"], "phase_id": "sustain_grow"},
    ],
    # Row 3 (Row 4 in visual)
    [
        {"id": "incentive_management", "name": "Incentive Management", "subtitle": CAPABILITY_DESCRIPTIONS["incentive_management"], "phase_id": "configure_price"},
        {"id": "customer_risk_fraud", "name": "Customer Risk and Fraud Check", "subtitle": CAPABILITY_DESCRIPTIONS["customer_risk_fraud"], "phase_id": "quote_sell"},
        {"id": "usage_data_mediation", "name": "Usage Data Mediation", "subtitle": CAPABILITY_DESCRIPTIONS["usage_data_mediation"], "phase_id": "invoice"},
        {"id": "collections", "name": "Collections", "subtitle": CAPABILITY_DESCRIPTIONS["collections"], "phase_id": "collect"},
        {"id": "deployment_provisioning", "name": "Deployment / Provisioning", "subtitle": CAPABILITY_DESCRIPTIONS["deployment_provisioning"], "phase_id": "provision"},
        {"id": "reporting_dashboards", "name": "Reporting and Dashboards", "subtitle": CAPABILITY_DESCRIPTIONS["reporting_dashboards"], "phase_id": "recognize_report"},
        {"id": "customer_value_intelligence", "name": "Customer Value Intelligence", "subtitle": CAPABILITY_DESCRIPTIONS["customer_value_intelligence"], "phase_id": "learn"},
        None,  # Empty cell
    ],
    # Row 4 (Row 5 in visual)
    [
        {"id": "channel_management", "name": "Channel Management", "subtitle": CAPABILITY_DESCRIPTIONS["channel_management"], "phase_id": "configure_price"},
        {"id": "contract_management", "name": "Contract Management", "subtitle": CAPABILITY_DESCRIPTIONS["contract_management"], "phase_id": "quote_sell"},
        {"id": "anomaly_detection", "name": "Anomaly Detection", "subtitle": CAPABILITY_DESCRIPTIONS["anomaly_detection"], "phase_id": "invoice"},
        {"id": "partner_settlement", "name": "Partner Settlement", "subtitle": CAPABILITY_DESCRIPTIONS["partner_settlement"], "phase_id": "collect"},
        None,  # Empty cell
        {"id": "tax", "name": "Tax", "subtitle": CAPABILITY_DESCRIPTIONS["tax"], "phase_id": "recognize_report"},
        {"id": "price_profit_optimization", "name": "Price/Profit Optimization", "subtitle": CAPABILITY_DESCRIPTIONS["price_profit_optimization"], "phase_id": "learn"},
        None,  # Empty cell
    ],
    # Row 5 (Row 6 in visual)
    [
        None,  # Empty cell
        {"id": "inventory_ship_availability", "name": "Inventory/Ship Availability", "subtitle": CAPABILITY_DESCRIPTIONS["inventory_ship_availability"], "phase_id": "quote_sell"},
        {"id": "dispute_prediction", "name": "Dispute Prediction", "subtitle": CAPABILITY_DESCRIPTIONS["dispute_prediction"], "phase_id": "invoice"},
        None,  # Empty cell
        None,  # Empty cell
        {"id": "compliance", "name": "Compliance", "subtitle": CAPABILITY_DESCRIPTIONS["compliance"], "phase_id": "recognize_report"},
        {"id": "partner_channel_intelligence", "name": "Partner/Channel Intelligence", "subtitle": CAPABILITY_DESCRIPTIONS["partner_channel_intelligence"], "phase_id": "learn"},
        None,  # Empty cell
    ],
    # Row 6 (Row 7 in visual)
    [
        None,  # Empty cell
        None,  # Empty cell
        None,  # Empty cell
        None,  # Empty cell
        None,  # Empty cell
        None,  # Empty cell
        {"id": "benchmarks", "name": "Benchmarks", "subtitle": CAPABILITY_DESCRIPTIONS["benchmarks"], "phase_id": "learn"},
        None,  # Empty cell
    ],
]

# Flatten to get all active capabilities
def get_all_capabilities():
    """Return list of all non-empty capabilities with their grid positions."""
    capabilities = []
    for row_idx, row in enumerate(GRID_LAYOUT):
        for col_idx, cell in enumerate(row):
            if cell is not None:
                capabilities.append({
                    **cell,
                    "row": row_idx,
                    "col": col_idx,
                    "phase_color": PHASES[col_idx]["color"]
                })
    return capabilities

def get_capability_by_id(cap_id: str):
    """Find capability by ID."""
    for row in GRID_LAYOUT:
        for cell in row:
            if cell and cell["id"] == cap_id:
                return cell
    return None

def get_capabilities_by_phase(phase_id: str):
    """Get all capabilities for a phase."""
    return [cap for cap in get_all_capabilities() if cap["phase_id"] == phase_id]

def get_phase_by_col(col: int):
    """Get phase info by column index."""
    return PHASES[col] if 0 <= col < len(PHASES) else None

# Statistics
TOTAL_CAPABILITIES = len(get_all_capabilities())  # Should be 38
TOTAL_CELLS = 7 * 8  # 56
EMPTY_CELLS = TOTAL_CELLS - TOTAL_CAPABILITIES  # Should be 18

# Capability ID to display name mapping
CAPABILITY_NAMES = {cap["id"]: cap["name"] for cap in get_all_capabilities()}

# Score styling
IMPORTANCE_STYLE = {
    "bg_color": "#fce4ec",
    "border_color": "#E6007E",
    "label_bg": "#E6007E"
}

READINESS_STYLE = {
    "bg_color": "#e0f7fa",
    "border_color": "#00A5A8",
    "label_bg": "#00A5A8"
}

# Full descriptions for tooltips
CAPABILITY_DESCRIPTIONS_FULL = {
    # 1. Configure and Price
    "offer_catalog_management": """Defines and maintains the full product and offer catalog: what you sell, how it's packaged, which usage metrics are tracked, and which promotions or bundles apply. This is where you decide how trials, bundles, add-ons, and tiered offers are structured so every downstream system sees a single, consistent definition of "the offer." """,

    "price_management": """Designs and governs the rules for how you price—list price vs. negotiated, regional differences, currency handling, and discount policies. The goal is to avoid one-off spreadsheets and ensure every channel (sales, ecommerce, partners) uses the same pricing logic so quotes, invoices, and revenue all line up.""",

    "revenue_planning": """Uses pipeline, pricing, and usage assumptions to simulate how new offers or price changes will affect revenue, margin, and cash over time. It supports FP&A in answering questions like, "If we introduce this new usage-based plan, what happens to ARR and gross margin over the next 12–24 months?" """,

    "incentive_management": """Defines rules for discounts, rebates, credits, and promotions across customers, segments, and channels. This includes eligibility rules, caps, and accrual logic so that incentives drive desired behavior (adoption, upsell, retention) while staying financially controlled and auditable.""",

    "channel_management": """Sets up and governs how offers, prices, and incentives are exposed through partners, resellers, marketplaces, and other indirect channels. It ensures partners see channel-appropriate products and pricing, and that downstream settlement and margin sharing are calculable and enforceable.""",

    # 2. Quote and Sell
    "opportunity_capture": """Brings together demand signals and deal data from web storefronts, CRM systems, and partner tools into a single opportunity view. This is where leads turn into structured opportunities with clear products, quantities, and pricing that can move into quoting and contracting.""",

    "customer_partner_portals": """Provide web experiences where customers and partners can view offers, configure orders, request quotes, and manage their own subscriptions. These portals reduce sales and support load by letting users trial, buy, upgrade, or renew without needing a rep for every transaction.""",

    "guided_selling": """Uses CPQ tools and rules to walk sellers—or customers themselves—through product selection, configuration, and pricing, while enforcing compatibility and discount policies. Price guidance layers in analytics or AI to recommend optimal prices and structures that balance win-rate, margin, and long-term value.""",

    "customer_risk_fraud": """Screens buyers and transactions for credit risk and potential fraud by combining internal history (payments, disputes) with external data (credit scores, fraud signals). The intent is to catch risky deals early, adjust terms (e.g., prepay, deposits), or block high-risk transactions before they become revenue leakage or bad debt.""",

    "contract_management": """Creates, negotiates, and stores customer contracts, including terms for pricing, usage, SLAs, renewals, and termination. It tracks versions, approvals, and signatures so that what sales promises, what billing charges, and what revenue recognizes are all derived from the same legal source of truth.""",

    "inventory_ship_availability": """For businesses with physical goods or constrained capacity, this ties quoting and ordering to actual availability. It answers "Can we deliver this by the promised date?" by checking current and projected inventory or capacity, and feeds that back into the quote or lead time presented to the customer.""",

    # 3. Invoice
    "order_management": """Turns accepted quotes or online orders into structured, executable orders that systems can act on. It sequences what should be provisioned, billed, and fulfilled, and tracks the lifecycle of that order through changes like upgrades, cancellations, or partial shipments.""",

    "billing_invoice": """Converts order and subscription data into accurate invoices on the right schedule (recurring, one-time, usage-based). It applies the correct taxes, discounts, and currencies, groups charges logically, and delivers invoices through the right channels (email, EDI, portals).""",

    "rating_charging": """Takes raw usage events (API calls, seats, minutes, GB, rides, etc.) and applies pricing rules (tiers, volume, overage, minimum commitments) to compute what to charge. This is the core engine that ensures customers are billed correctly for how they actually used the service.""",

    "usage_data_mediation": """Ingests noisy, high-volume usage data from multiple sources and normalizes it into clean, billable records. It handles mapping, enrichment, de-duplication, and aggregation (e.g., daily or monthly totals) so the rating engine can work reliably and auditors can trace charges back to source data.""",

    "anomaly_detection": """Monitors usage and billing patterns to spot unexpected spikes, drops, or irregularities in charges, invoices, or revenue. It helps catch configuration errors, data issues, or abusive behavior before they result in customer complaints, disputes, or material misstatements.""",

    "dispute_prediction": """Uses historical behavior and patterns to flag invoices or accounts that are likely to be challenged by customers. This allows finance or customer success to proactively review, adjust, or reach out, reducing escalations, aging AR, and friction with key accounts.""",

    # 4. Collect
    "payment_routing": """Orchestrates how payments are initiated, authorized, and settled across gateways, methods (card, ACH, wallets, wires), and regions. It decides which gateway to route a transaction to, how to handle retries, and how to optimize for approval rates and transaction costs.""",

    "customer_credit_management": """Assesses and tracks each customer's ability and willingness to pay, often via credit limits, scoring, and payment history. It informs terms like prepayment, deposits, or invoice frequency and helps prevent over-extension that could turn into bad debt.""",

    "dunning_payment_retry": """Implements automated sequences for handling failed or late payments—smart retry schedules, reminder emails, messaging, and escalation paths. The goal is to recover revenue non-confrontationally while keeping the customer experience positive.""",

    "collections": """Coordinates more intensive recovery efforts for seriously overdue receivables, including internal teams and, where needed, external agencies. It structures repayment plans, settlements, or service suspensions in a way that maximizes recovery while protecting relationships and compliance.""",

    "partner_settlement": """Calculates and pays out what's owed to partners—commissions, revenue shares, rebates, or referral fees—based on actual transactions and agreed commercial terms. It provides transparency to partners and ensures accurate recognition of both revenue and associated costs.""",

    # 5. Provision
    "entitlement_management": """Controls which products, features, or service levels each customer can actually use once they've bought. It ties contracts and subscriptions to real-world access—APIs, seats, environments, or content—so that only entitled customers see or consume what they've paid for.""",

    "inventory": """Maintains an up-to-date view of what is available to sell or allocate—whether it's physical devices, licenses, IP ranges, or capacity units. It helps prevent overselling and informs both fulfillment and future planning.""",

    "fulfillment_ship": """Manages the operational steps to deliver the product or service—picking, packing, shipping, activating, or assigning. It integrates with logistics and internal systems so that once an order is placed, the right actions happen in the right sequence with traceability.""",

    "deployment_provisioning": """Automates the technical activation steps: creating accounts, enabling features, configuring environments, or connecting integrations. It ensures customers can start using what they've bought quickly and consistently, with minimal manual setup.""",

    # 6. Recognize and Report
    "revenue_recognition": """Applies rules like ASC 606 / IFRS 15 to determine when and how revenue should be recognized based on performance obligations, delivery, and contract changes. It manages schedules, reallocations, and remeasurements so reported revenue accurately reflects the economics of the deals.""",

    "accounting_ledger": """Posts the correct journal entries for billing, payments, revenue, taxes, and adjustments into the general ledger or subledgers. This is the bridge between operational systems (billing, orders) and formal financial statements.""",

    "usage_entitlement_enforcement": """Monitors actual usage and entitlements to make sure customers are operating within the terms of their contracts. It can enforce hard limits, soft warnings, or overage rules, and provides data back to sales and finance for true-up, expansion, or renegotiation.""",

    "reporting_dashboards": """Aggregates metrics across the lifecycle—MRR/ARR, churn, cohort behavior, DSO, margins, product performance—and presents them in accessible dashboards. This gives leadership and teams a single, trusted view of how the business is performing.""",

    "tax": """Calculates and applies the right indirect taxes (VAT, GST, sales tax, digital services taxes, etc.) based on jurisdiction, product type, and customer profile. It integrates with tax engines and maintains the records needed for filings and audits.""",

    "compliance": """Ensures processes and data handling follow relevant regulations—financial (SOX), privacy (GDPR/CCPA), industry standards, and internal policies. This includes audit trails, segregation of duties, and documented controls across the monetization stack.""",

    # 7. Learn
    "revenue_profit_insights": """Looks beyond top-line revenue to understand margins, unit economics, and profitability by product, segment, and channel. It answers "Where are we really making or losing money?" and informs both strategy and tactical actions.""",

    "customer_insights": """Combines product usage, billing behavior, support interactions, and engagement to identify at-risk customers and those with expansion potential. It powers health scores and next-best-action models for customer success and marketing.""",

    "offer_insights": """Analyzes how particular offers, bundles, discounts, and pricing structures perform across segments and cohorts. It shows which offers drive high LTV and which ones lead to churn, discount addiction, or low margins.""",

    "customer_value_intelligence": """Creates a holistic view of customer value over time—combining what they pay, how they use the product, their cost-to-serve, and their credit or risk profile. This supports segmentation, prioritization, and tailored strategies by customer group.""",

    "price_profit_optimization": """Uses data and experimentation to refine price levels, structures, and discount policies. It helps identify where you're under-pricing, over-discounting, or leaving value on the table, and guides adjustments that improve both win-rate and profitability.""",

    "partner_channel_intelligence": """Evaluates how different partners and channels contribute to growth, margin, and retention. It surfaces which routes to market are most effective, where enablement or cleanup is needed, and how incentives should be tuned.""",

    "benchmarks": """Places your metrics in context by comparing them to peer or industry benchmarks—churn, growth, ARPU, collection efficiency, etc. This helps identify where you're leading, lagging, or simply average, and where change is most urgent.""",

    # 8. Sustain and Grow
    "churn_prevent": """Uses churn predictions and early warning signals to trigger proactive actions—targeted offers, plan adjustments, outreach, or service changes—to keep customers from leaving. For those who do churn, it designs win-back campaigns that are economically rational.""",

    "renewals": """Treats renewal as a structured selling motion, not an afterthought—using CPQ and analytics to propose the right combination of term, price, and expansion at renewal time. It supports auto-renew for simple deals and guided, value-based conversations for complex ones.""",

    "customer_success": """Coordinates the people, processes, and digital touchpoints that keep customers successful post-sale—onboarding, training, QBRs, and ongoing health checks. It closes the loop with product, pricing, and sales by feeding back what's working and where customers struggle.""",
}


def get_capability_full_description(cap_id: str) -> str:
    """Get full description for a capability."""
    return CAPABILITY_DESCRIPTIONS_FULL.get(cap_id, "No description available.")
