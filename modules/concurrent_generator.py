# modules/concurrent_generator.py
import concurrent.futures
from datetime import datetime
from typing import Dict, List

from modules.score_analyzer import analyze_capabilities, create_priority_matrix, get_capabilities_by_category
from modules.report_generator import (
    synthesize_with_claude,
    format_gap_context,
    format_executive_context,
    find_capability_in_kb,
    filter_by_importance_threshold,
    MCP_GUIDE_SECTION,
    AGENT_GUIDE_SECTION,
    VALID_AGENTS
)


def generate_priority_matrix_table(analyzed_capabilities: List[Dict]) -> str:
    """Generate priority matrix table from analyzed capabilities."""
    categories = {
        "URGENT_GAP": 0,
        "CRITICAL_GAP": 0,
        "STRENGTH": 0,
        "OPPORTUNITY": 0,
        "MAINTAIN": 0,
        "DEPRIORITIZE": 0
    }

    for cap in analyzed_capabilities:
        cat = cap.get("priority_category", "MAINTAIN")
        categories[cat] = categories.get(cat, 0) + 1

    table = "| Priority | Count |\n|----------|-------|\n"
    table += f"| 🔴 Urgent Gaps | {categories['URGENT_GAP']} |\n"
    table += f"| 🟠 Critical Gaps | {categories['CRITICAL_GAP']} |\n"
    table += f"| 🟢 Strengths | {categories['STRENGTH']} |\n"
    table += f"| 🟡 Opportunities | {categories['OPPORTUNITY']} |\n"
    table += f"| 🔵 Maintain | {categories['MAINTAIN']} |\n"
    table += f"| ⚪ Deprioritize | {categories['DEPRIORITIZE']} |\n"

    return table


def generate_report_concurrent(
    scores: List[Dict],
    knowledge_base: dict,
    company_name: str,
    max_workers: int = 3
) -> str:
    """
    Generate report with concurrent section processing.

    Splits synthesis into parallel tasks for:
    - Executive summary
    - Each urgent gap (parallel)
    - MCP sections (static, no wait)
    """

    # Step 1: Compute priorities (fast, no LLM)
    analyzed = analyze_capabilities(scores, knowledge_base)
    analyzed = filter_by_importance_threshold(analyzed)

    # Get urgent gaps
    urgent_gaps = get_capabilities_by_category(analyzed, "URGENT_GAP")
    critical_gaps = get_capabilities_by_category(analyzed, "CRITICAL_GAP")

    # Calculate metrics
    all_i = [s['importance'] for s in analyzed]
    all_r = [s['readiness'] for s in analyzed]
    avg_importance = sum(all_i) / len(all_i) if all_i else 0
    avg_readiness = sum(all_r) / len(all_r) if all_r else 0

    # Step 2: Prepare all synthesis tasks
    tasks = []

    # Executive summary task
    exec_context = format_executive_context(
        company_name, len(analyzed), urgent_gaps, critical_gaps,
        avg_importance, avg_readiness
    )
    tasks.append(("executive_summary", exec_context))

    # Gap tasks (one per gap)
    for gap in urgent_gaps[:10]:  # Limit to top 10 urgent gaps
        kb_data = find_capability_in_kb(gap['capability_id'], knowledge_base)
        if kb_data:
            context = format_gap_context(gap, kb_data)
            tasks.append((f"gap_{gap['capability_id']}", context, gap))

    # Step 3: Run synthesis concurrently
    results = {}

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_task = {}

        for task in tasks:
            if task[0] == "executive_summary":
                future = executor.submit(
                    synthesize_with_claude,
                    "executive_summary",
                    task[1],
                    VALID_AGENTS
                )
                future_to_task[future] = ("executive_summary", None)
            else:
                future = executor.submit(
                    synthesize_with_claude,
                    "urgent_gap",
                    task[1],
                    VALID_AGENTS
                )
                future_to_task[future] = ("gap", task[2])

        # Collect results as they complete
        for future in concurrent.futures.as_completed(future_to_task):
            task_type, gap_data = future_to_task[future]
            try:
                result = future.result()
                if task_type == "executive_summary":
                    results["executive_summary"] = result
                else:
                    results[gap_data['capability_id']] = {
                        "gap": gap_data,
                        "synthesis": result
                    }
            except Exception as e:
                print(f"Synthesis error: {e}")

    # Step 4: Assemble report
    urgent_sections = []
    for gap in urgent_gaps[:10]:
        if gap['capability_id'] in results:
            gap_result = results[gap['capability_id']]
            section = f"""### {gap['capability_name']}
**Phase:** {gap['phase_name']} | **Scores:** I={gap['importance']}, R={gap['readiness']}, Gap={gap.get('gap_score', 0)}

{gap_result['synthesis']}
"""
            urgent_sections.append(section)

    report = f"""# O2C AI & MCP Readiness Assessment
## {company_name}
*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*

---

## 1. Executive Summary

{results.get('executive_summary', 'Unable to generate summary.')}

---

## 2. Priority Matrix

{generate_priority_matrix_table(analyzed)}

---

## 3. Urgent Gaps - Detailed Analysis

{chr(10).join(urgent_sections) if urgent_sections else "*No urgent gaps identified.*"}

---

## 4. Getting Started with Zuora MCP

{MCP_GUIDE_SECTION}

---

## 5. Building Your First Zuora Agent

{AGENT_GUIDE_SECTION}
"""

    return report
