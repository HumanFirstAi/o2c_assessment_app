from typing import Dict, List
import json
import config

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
    if importance <= config.IMPORTANCE_LOW_THRESHOLD:
        return "DEPRIORITIZE"
    elif importance >= config.IMPORTANCE_HIGH_THRESHOLD:
        if readiness <= config.READINESS_LOW_THRESHOLD:
            return "URGENT_GAP"
        elif readiness <= 6:
            return "CRITICAL_GAP"
        else:
            return "STRENGTH"
    else:  # Medium importance (4-6)
        if readiness <= config.READINESS_LOW_THRESHOLD:
            return "OPPORTUNITY"
        else:
            return "MAINTAIN"


def calculate_gap_score(importance: int, readiness: int) -> int:
    """
    Calculate gap score for prioritization.
    Higher score = more urgent.
    Formula: importance * (10 - readiness) / 10, rounded to integer
    """
    return round(importance * (10 - readiness) / 10)


def analyze_capabilities(scores: List[Dict], knowledge_base: dict) -> List[Dict]:
    """
    Analyze each capability by combining scores with knowledge base data.
    Returns list of enriched capability analyses.
    """
    analyzed = []

    # Create a lookup for capabilities in knowledge base
    kb_capabilities = {}
    for phase in knowledge_base.get("phases", []):
        for cap in phase.get("capabilities", []):
            kb_capabilities[cap["id"]] = {
                **cap,
                "phase_name": phase["name"],
                "phase_id": phase["id"],
                "phase_color": phase["color"],
                "agentic_goal": phase["agentic_goal"]
            }

    for score_data in scores:
        capability_id = score_data.get("capability_id")
        importance = score_data.get("importance", 5)
        readiness = score_data.get("readiness", 5)

        # Get KB data for this capability
        kb_data = kb_capabilities.get(capability_id, {})

        # Calculate priority
        priority_category = categorize_priority(importance, readiness)
        gap_score = calculate_gap_score(importance, readiness)
        timeline_info = TIMELINE_MAPPING.get(priority_category, {})

        analyzed.append({
            "capability_id": capability_id,
            "capability_name": kb_data.get("name", "Unknown"),
            "phase_name": kb_data.get("phase_name", "Unknown"),
            "phase_id": kb_data.get("phase_id", ""),
            "phase_color": kb_data.get("phase_color", "#000000"),
            "importance": importance,
            "readiness": readiness,
            "priority_category": priority_category,
            "gap_score": gap_score,
            "timeline": timeline_info.get("horizon", ""),
            "agent_tier": timeline_info.get("agent_tier", ""),
            "investment": timeline_info.get("investment", ""),
            "why_it_matters": kb_data.get("why_it_matters", ""),
            "current_ai_capabilities": kb_data.get("current_ai_capabilities", {}),
            "whats_coming": kb_data.get("whats_coming", {}),
            "agent_mapping": kb_data.get("agent_mapping", {}),
            "row": kb_data.get("row", 0),
            "col": kb_data.get("col", 0)
        })

    # Sort by gap_score descending (most urgent first)
    analyzed.sort(key=lambda x: x["gap_score"], reverse=True)

    return analyzed


def create_priority_matrix(analyzed_capabilities: List[Dict]) -> Dict[str, int]:
    """
    Create a summary count of capabilities in each priority category.
    """
    matrix = {
        "URGENT_GAP": 0,
        "CRITICAL_GAP": 0,
        "STRENGTH": 0,
        "OPPORTUNITY": 0,
        "MAINTAIN": 0,
        "DEPRIORITIZE": 0
    }

    for cap in analyzed_capabilities:
        category = cap.get("priority_category", "MAINTAIN")
        matrix[category] = matrix.get(category, 0) + 1

    return matrix


def get_capabilities_by_category(
    analyzed_capabilities: List[Dict],
    category: str
) -> List[Dict]:
    """
    Filter capabilities by priority category.
    """
    return [
        cap for cap in analyzed_capabilities
        if cap.get("priority_category") == category
    ]


def get_phase_summary(analyzed_capabilities: List[Dict]) -> Dict[str, Dict]:
    """
    Create a summary of capabilities grouped by phase.
    """
    phase_summary = {}

    for cap in analyzed_capabilities:
        phase_id = cap.get("phase_id")
        phase_name = cap.get("phase_name")

        if phase_id not in phase_summary:
            phase_summary[phase_id] = {
                "phase_name": phase_name,
                "capabilities": [],
                "avg_importance": 0,
                "avg_readiness": 0,
                "avg_gap_score": 0,
                "urgent_count": 0,
                "strength_count": 0
            }

        phase_summary[phase_id]["capabilities"].append(cap)

        # Track counts
        if cap.get("priority_category") == "URGENT_GAP":
            phase_summary[phase_id]["urgent_count"] += 1
        elif cap.get("priority_category") == "STRENGTH":
            phase_summary[phase_id]["strength_count"] += 1

    # Calculate averages for each phase
    for phase_id, data in phase_summary.items():
        caps = data["capabilities"]
        if caps:
            data["avg_importance"] = sum(c["importance"] for c in caps) / len(caps)
            data["avg_readiness"] = sum(c["readiness"] for c in caps) / len(caps)
            data["avg_gap_score"] = round(sum(c["gap_score"] for c in caps) / len(caps))

    return phase_summary
