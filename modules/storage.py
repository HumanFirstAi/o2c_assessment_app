# modules/storage.py
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional
import hashlib

from config import USER_DATA_DIR

# Storage directory - uses Railway Volume at /data
STORAGE_DIR = Path(USER_DATA_DIR)


def get_user_storage_path(email: str) -> Path:
    """Get storage directory for a user."""
    safe_email = hashlib.md5(email.encode()).hexdigest()[:16]
    user_dir = STORAGE_DIR / safe_email
    user_dir.mkdir(parents=True, exist_ok=True)
    return user_dir


def save_assessment(user: dict, scores: dict, report: str) -> str:
    """Save user's assessment and report."""
    user_dir = get_user_storage_path(user["email"])

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    assessment_id = f"{timestamp}_{user['session_id']}"

    # Save scores
    scores_file = user_dir / f"scores_{assessment_id}.json"
    scores_data = {
        "assessment_id": assessment_id,
        "user": user,
        "timestamp": datetime.now().isoformat(),
        "scores": scores
    }
    with open(scores_file, "w") as f:
        json.dump(scores_data, f, indent=2)

    # Save report
    report_file = user_dir / f"report_{assessment_id}.md"
    with open(report_file, "w") as f:
        f.write(report)

    return assessment_id


def get_user_assessments(email: str) -> list:
    """Get all assessments for a user."""
    user_dir = get_user_storage_path(email)

    assessments = []
    for scores_file in user_dir.glob("scores_*.json"):
        with open(scores_file) as f:
            data = json.load(f)
            assessments.append({
                "id": data["assessment_id"],
                "timestamp": data["timestamp"],
                "scores_file": str(scores_file),
                "report_file": str(scores_file).replace("scores_", "report_").replace(".json", ".md")
            })

    # Sort by timestamp descending
    assessments.sort(key=lambda x: x["timestamp"], reverse=True)
    return assessments


def load_assessment(email: str, assessment_id: str) -> Optional[dict]:
    """Load a specific assessment."""
    user_dir = get_user_storage_path(email)

    scores_file = user_dir / f"scores_{assessment_id}.json"
    report_file = user_dir / f"report_{assessment_id}.md"

    if not scores_file.exists():
        return None

    with open(scores_file) as f:
        data = json.load(f)

    if report_file.exists():
        with open(report_file) as f:
            data["report"] = f.read()

    return data
