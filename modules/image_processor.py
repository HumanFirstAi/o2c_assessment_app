import anthropic
import base64
import json
from pathlib import Path
from typing import Tuple, Dict, List
import config

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


def extract_scores_from_image(image_path: str) -> Tuple[Dict, List[str]]:
    """
    Use Claude Vision to extract I/R scores from assessment image.
    Returns tuple of (extracted data dict, warnings list)
    """
    client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)

    # Determine media type from file extension
    path = Path(image_path)
    ext = path.suffix.lower()
    if ext in ['.jpg', '.jpeg']:
        media_type = "image/jpeg"
    elif ext == '.png':
        media_type = "image/png"
    elif ext == '.gif':
        media_type = "image/gif"
    elif ext == '.webp':
        media_type = "image/webp"
    else:
        media_type = "image/png"  # default

    with open(image_path, "rb") as f:
        image_data = base64.standard_b64encode(f.read()).decode("utf-8")

    message = client.messages.create(
        model=config.CLAUDE_MODEL,
        max_tokens=4096,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
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

    extracted_data = parse_extraction_response(message.content[0].text)
    validated_data, warnings = validate_scores(extracted_data)

    return validated_data, warnings


def parse_extraction_response(response_text: str) -> dict:
    """
    Parse the JSON response from Claude Vision.
    """
    try:
        # Try to find JSON in the response
        # Sometimes Claude wraps JSON in markdown code blocks
        if "```json" in response_text:
            start = response_text.find("```json") + 7
            end = response_text.find("```", start)
            json_str = response_text[start:end].strip()
        elif "```" in response_text:
            start = response_text.find("```") + 3
            end = response_text.find("```", start)
            json_str = response_text[start:end].strip()
        else:
            json_str = response_text.strip()

        data = json.loads(json_str)
        return data
    except json.JSONDecodeError as e:
        # Fallback: return empty structure
        return {
            "scores": [],
            "extraction_confidence": "low",
            "notes": f"Failed to parse JSON response: {str(e)}"
        }


def validate_scores(extracted_scores: dict) -> Tuple[dict, List[str]]:
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
            warnings.append(f"{score.get('capability', 'Unknown')}: Invalid importance score {imp}")
            imp = max(1, min(10, imp))  # Clamp

        if rdy is not None and not (1 <= rdy <= 10):
            warnings.append(f"{score.get('capability', 'Unknown')}: Invalid readiness score {rdy}")
            rdy = max(1, min(10, rdy))

        # Only include if both scores are present
        if imp is not None and rdy is not None:
            validated.append({
                **score,
                "importance": imp,
                "readiness": rdy
            })
        else:
            warnings.append(f"{score.get('capability', 'Unknown')}: Missing scores (I={imp}, R={rdy})")

    # Add confidence and notes to warnings if present
    if extracted_scores.get("extraction_confidence") == "low":
        warnings.append("Low extraction confidence - please review scores carefully")

    if extracted_scores.get("notes"):
        warnings.append(f"Extraction notes: {extracted_scores['notes']}")

    return {"scores": validated}, warnings
