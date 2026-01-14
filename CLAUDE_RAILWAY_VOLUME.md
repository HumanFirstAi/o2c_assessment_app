# CLAUDE.md - Railway Volume Storage

## Task

Configure the app to use Railway Volume for persistent storage.

---

## 1. Attach Volume in Railway Dashboard

**Manual step (do this in Railway dashboard):**

1. Go to railway.app → Your Project
2. Click your service
3. Go to **Settings** tab → **Volumes**
4. Click **"Add Volume"**
5. Set:
   - **Mount Path:** `/data`
   - **Size:** 1GB (can expand later)
6. Click **Save**
7. Redeploy

---

## 2. Update config.py

```python
import os

# Storage paths - use Railway Volume mount
STORAGE_BASE = os.getenv("STORAGE_PATH", "/data")

# Subdirectories
USER_DATA_DIR = os.path.join(STORAGE_BASE, "user_data")
USER_LOGS_DIR = os.path.join(STORAGE_BASE, "user_logs")

# Create directories on startup
os.makedirs(USER_DATA_DIR, exist_ok=True)
os.makedirs(USER_LOGS_DIR, exist_ok=True)
```

---

## 3. Update modules/storage.py

Change the storage directory to use the volume:

```python
import os
from pathlib import Path
from config import USER_DATA_DIR, USER_LOGS_DIR

# CHANGE FROM:
# STORAGE_DIR = Path("user_data")

# CHANGE TO:
STORAGE_DIR = Path(USER_DATA_DIR)


def get_user_storage_path(email: str) -> Path:
    """Get storage directory for a user."""
    import hashlib
    safe_email = hashlib.md5(email.encode()).hexdigest()[:16]
    user_dir = STORAGE_DIR / safe_email
    user_dir.mkdir(parents=True, exist_ok=True)
    return user_dir
```

---

## 4. Update modules/auth.py

Change log directory:

```python
from config import USER_LOGS_DIR
from pathlib import Path

def log_user_activity(user: dict, activity: str, data: dict = None):
    """Log user activity to volume."""
    log_dir = Path(USER_LOGS_DIR)
    log_dir.mkdir(exist_ok=True)
    
    # ... rest of function stays the same
```

---

## 5. Add Environment Variable in Railway

In Railway dashboard → Variables:

```
STORAGE_PATH=/data
```

---

## 6. Local Development Fallback

For local development (no volume), it falls back to local directories:

```python
# config.py handles this automatically
STORAGE_BASE = os.getenv("STORAGE_PATH", "/data")

# Locally, create /data or use current directory
if not os.path.exists(STORAGE_BASE):
    STORAGE_BASE = os.path.join(os.getcwd(), "data")
    os.makedirs(STORAGE_BASE, exist_ok=True)
```

---

## Final config.py

```python
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Railway provides PORT
PORT = os.getenv("PORT", "8501")

# Environment
ENV = os.getenv("ENV", "development")
IS_PRODUCTION = ENV == "production"

# Claude API
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-opus-4-20250514")
CLAUDE_MAX_TOKENS = int(os.getenv("CLAUDE_MAX_TOKENS", "2000"))

# Storage - Railway Volume or local fallback
STORAGE_BASE = os.getenv("STORAGE_PATH", "/data")

# Local fallback if /data doesn't exist
if not os.path.exists(STORAGE_BASE) and not IS_PRODUCTION:
    STORAGE_BASE = os.path.join(os.getcwd(), "local_data")

# Storage directories
USER_DATA_DIR = os.path.join(STORAGE_BASE, "user_data")
USER_LOGS_DIR = os.path.join(STORAGE_BASE, "user_logs")

# Create on startup
Path(USER_DATA_DIR).mkdir(parents=True, exist_ok=True)
Path(USER_LOGS_DIR).mkdir(parents=True, exist_ok=True)

# Validate in production
if IS_PRODUCTION and not ANTHROPIC_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY required")
```

---

## Storage Structure on Volume

```
/data/                      # Railway Volume mount
├── user_data/
│   ├── a1b2c3d4e5f6/      # User 1 (hashed email)
│   │   ├── scores_20250114_120000.json
│   │   └── report_20250114_120000.md
│   └── f6e5d4c3b2a1/      # User 2
│       └── ...
└── user_logs/
    ├── activity_2025-01-14.jsonl
    └── activity_2025-01-15.jsonl
```

---

## Railway Setup Summary

1. **Dashboard:** Add Volume with mount path `/data`
2. **Variables:** Add `STORAGE_PATH=/data`
3. **Deploy:** `railway up`

Data now persists across deploys.

---

## Verify Storage

After deploy, check logs:

```bash
railway logs | grep "data"
```

Or add a health check in app.py:

```python
# At startup
import os
from config import USER_DATA_DIR

if os.path.exists(USER_DATA_DIR):
    print(f"✅ Storage mounted: {USER_DATA_DIR}")
else:
    print(f"⚠️ Storage not found: {USER_DATA_DIR}")
```
