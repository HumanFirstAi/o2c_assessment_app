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

# Storage - Railway Volume or local fallback
STORAGE_BASE = os.getenv("STORAGE_PATH", "/data")

# Local fallback if /data doesn't exist (for development)
if not os.path.exists(STORAGE_BASE) and not IS_PRODUCTION:
    STORAGE_BASE = os.path.join(os.getcwd(), "local_data")

# Storage directories
USER_DATA_DIR = os.path.join(STORAGE_BASE, "user_data")
USER_LOGS_DIR = os.path.join(STORAGE_BASE, "user_logs")

# Create directories on startup
Path(USER_DATA_DIR).mkdir(parents=True, exist_ok=True)
Path(USER_LOGS_DIR).mkdir(parents=True, exist_ok=True)

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
