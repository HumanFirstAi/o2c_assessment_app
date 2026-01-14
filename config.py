import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Railway Configuration
PORT = os.getenv("PORT", "8501")

# Environment
ENV = os.getenv("ENV", "development")
IS_PRODUCTION = ENV == "production"

# API Configuration
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-opus-4-20250514")
CLAUDE_MAX_TOKENS = int(os.getenv("CLAUDE_MAX_TOKENS", "2000"))

# Validate in production
if IS_PRODUCTION and not ANTHROPIC_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY environment variable required in production")

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
