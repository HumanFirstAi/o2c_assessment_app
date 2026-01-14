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
