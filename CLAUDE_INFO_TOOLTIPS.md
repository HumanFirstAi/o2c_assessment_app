# CLAUDE.md - Capability Info Tooltips

## Task

Add an information icon (ℹ️) to each capability card that shows the full description on hover.

---

## 1. Create Capability Descriptions Dictionary

**Add to grid_layout.py:**

```python
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
```

---

## 2. Update Card HTML with Tooltip

**In modules/interactive_form.py:**

```python
from grid_layout import get_capability_full_description

def render_capability_card(cell, row_idx, col_idx):
    """Render capability card with info tooltip."""
    cap_id = cell['id']
    full_desc = get_capability_full_description(cap_id)
    
    # Escape quotes for HTML attribute
    full_desc_escaped = full_desc.replace('"', '&quot;').replace("'", "&#39;")
    
    card_html = f'''
    <div style="
        background: white; 
        border: 2px solid {border_color}; 
        border-radius: 4px; 
        padding: 10px; 
        height: 100px;
        min-height: 100px;
        max-height: 100px;
        overflow: hidden;
        position: relative;
    ">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div style="
                font-weight: 600; 
                font-size: 15px; 
                color: #333; 
                line-height: 1.2;
                flex: 1;
            ">
                {cell['name']}
            </div>
            <div class="tooltip-container" style="position: relative; cursor: help;">
                <span style="
                    font-size: 14px; 
                    color: #888;
                    margin-left: 4px;
                ">ℹ️</span>
                <div class="tooltip-content" style="
                    display: none;
                    position: absolute;
                    right: 0;
                    top: 20px;
                    width: 300px;
                    padding: 12px;
                    background: #1a1a1a;
                    color: #fff;
                    border-radius: 8px;
                    font-size: 12px;
                    font-weight: normal;
                    line-height: 1.5;
                    z-index: 1000;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
                ">
                    {full_desc_escaped}
                </div>
            </div>
        </div>
        <div style="
            font-size: 12px; 
            color: #888; 
            font-style: italic;
            line-height: 1.3;
            margin-top: 4px;
        ">
            {cell.get('subtitle', '')}
        </div>
    </div>
    '''
    
    return card_html
```

---

## 3. Add CSS for Tooltip Hover

**Add to app.py (at the top, after st.set_page_config):**

```python
st.markdown("""
<style>
/* Tooltip hover effect */
.tooltip-container:hover .tooltip-content {
    display: block !important;
}

/* Tooltip arrow */
.tooltip-content::before {
    content: '';
    position: absolute;
    top: -8px;
    right: 10px;
    border-width: 0 8px 8px 8px;
    border-style: solid;
    border-color: transparent transparent #1a1a1a transparent;
}

/* Ensure tooltip stays visible when hovering over it */
.tooltip-content:hover {
    display: block !important;
}
</style>
""", unsafe_allow_html=True)
```

---

## 4. Alternative: Using Streamlit's Native Tooltip

If CSS hover doesn't work well in Streamlit, use st.popover:

```python
def render_capability_card(cell, row_idx, col_idx):
    """Render capability card with popover info."""
    cap_id = cell['id']
    full_desc = get_capability_full_description(cap_id)
    
    # Card container
    with st.container():
        # Card HTML (without tooltip)
        card_html = f'''
        <div style="
            background: white; 
            border: 2px solid {border_color}; 
            border-radius: 4px; 
            padding: 10px; 
            height: 100px;
        ">
            <div style="font-weight: 600; font-size: 15px; color: #333;">
                {cell['name']}
            </div>
            <div style="font-size: 12px; color: #888; font-style: italic;">
                {cell.get('subtitle', '')}
            </div>
        </div>
        '''
        st.markdown(card_html, unsafe_allow_html=True)
        
        # Info popover button
        with st.popover("ℹ️", use_container_width=False):
            st.markdown(f"**{cell['name']}**")
            st.markdown(full_desc)
```

---

## 5. Alternative: Using st.help or Native Tooltip

```python
# Simpler approach using Streamlit columns
col1, col2 = st.columns([0.9, 0.1])

with col1:
    st.markdown(card_html, unsafe_allow_html=True)

with col2:
    st.button("ℹ️", key=f"info_{cap_id}", help=full_desc)
```

---

## Summary

| Change | Description |
|--------|-------------|
| Add descriptions dict | 38 full descriptions in grid_layout.py |
| Add info icon | ℹ️ in top-right of each card |
| Show tooltip on hover | CSS-based or st.popover |
| Tooltip content | Full capability description |

---

## Visual Result

```
┌─────────────────────────────┐
│ Customer and Partner    ℹ️  │  ← Hover shows full description
│ Portals                     │
│ Self-service interfaces.    │
└─────────────────────────────┘
```

On hover:
```
┌─────────────────────────────┐
│ Customer and Partner    ℹ️  │
│ Portals                     │
│ Self-service interfaces.    │
└──────────────┬──────────────┘
               │
    ┌──────────▼──────────────────────┐
    │ Provide web experiences where   │
    │ customers and partners can view │
    │ offers, configure orders,       │
    │ request quotes, and manage      │
    │ their own subscriptions...      │
    └─────────────────────────────────┘
```
