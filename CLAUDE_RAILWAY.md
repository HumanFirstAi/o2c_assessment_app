# CLAUDE.md - Railway Deployment Automation

## Task

Create automated deployment pipeline for Railway with CLI scripts.

## Files to Create

Create these 5 files in the project root:

---

### 1. railway.json

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true",
    "healthcheckPath": "/",
    "healthcheckTimeout": 300
  }
}
```

---

### 2. Procfile

```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true --server.enableCORS=false --server.enableXsrfProtection=false
```

---

### 3. .streamlit/config.toml

Create `.streamlit` directory if it doesn't exist.

```toml
[server]
headless = true
address = "0.0.0.0"
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false

[theme]
base = "dark"
```

---

### 4. deploy.sh

```bash
#!/bin/bash
set -e

echo "🚀 O2C Assessment App - Railway Deployment"
echo "==========================================="

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check Railway CLI installed
if ! command -v railway &> /dev/null; then
    echo -e "${YELLOW}Installing Railway CLI...${NC}"
    npm install -g @railway/cli
fi

# Check if logged in
if ! railway whoami &> /dev/null; then
    echo -e "${YELLOW}Please login to Railway:${NC}"
    railway login
fi

# Check for required environment variables
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo -e "${RED}Error: ANTHROPIC_API_KEY not set${NC}"
    echo "Run: export ANTHROPIC_API_KEY=sk-ant-xxxxx"
    exit 1
fi

# Initialize project if not already linked
if [ ! -f ".railway/config.json" ]; then
    echo -e "${YELLOW}Initializing Railway project...${NC}"
    railway init
fi

# Set environment variables
echo -e "${GREEN}Setting environment variables...${NC}"
railway variables set ANTHROPIC_API_KEY="$ANTHROPIC_API_KEY"
railway variables set CLAUDE_MODEL="claude-opus-4-20250514"
railway variables set CLAUDE_MAX_TOKENS="2000"
railway variables set ENV="production"

# Deploy
echo -e "${GREEN}Deploying to Railway...${NC}"
railway up --detach

# Get deployment URL
echo -e "${GREEN}Fetching deployment URL...${NC}"
sleep 5
railway open

echo ""
echo -e "${GREEN}✅ Deployment complete!${NC}"
echo "Run 'railway logs' to view logs"
echo "Run 'railway open' to open in browser"
```

---

### 5. Makefile

```makefile
.PHONY: setup deploy logs open status vars test local full redeploy

# Initial setup - create Railway config files
setup:
	@mkdir -p .streamlit
	@chmod +x deploy.sh
	@echo "✅ Setup complete"

# Deploy to Railway
deploy:
	@./deploy.sh

# View logs
logs:
	railway logs --tail 100

# Open in browser
open:
	railway open

# Check status
status:
	railway status

# List variables
vars:
	railway variables

# Run locally
local:
	streamlit run app.py

# Run test mode locally
test:
	streamlit run app.py &
	sleep 3
	open "http://localhost:8501/?test=mixed" 2>/dev/null || xdg-open "http://localhost:8501/?test=mixed" 2>/dev/null || echo "Open http://localhost:8501/?test=mixed"

# Full deploy (setup + deploy)
full: setup deploy

# Quick redeploy
redeploy:
	railway up --detach

# View domain
domain:
	railway domain
```

---

### 6. runtime.txt

```
python-3.11.0
```

---

### 7. .gitignore (update if exists)

Add these lines:

```
.env
.env.*
__pycache__/
*.pyc
.railway/
venv/
.venv/
*.log
.DS_Store
```

---

## Update config.py

Update or create config.py with Railway-compatible settings:

```python
import os
from dotenv import load_dotenv

load_dotenv()

# Railway provides PORT automatically
PORT = os.getenv("PORT", "8501")

# Environment
ENV = os.getenv("ENV", "development")
IS_PRODUCTION = ENV == "production"

# Claude API
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-opus-4-20250514")
CLAUDE_MAX_TOKENS = int(os.getenv("CLAUDE_MAX_TOKENS", "2000"))

# Validate in production
if IS_PRODUCTION and not ANTHROPIC_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY environment variable required")
```

---

## Update app.py

Add at the top of app.py (after imports):

```python
import os
from dotenv import load_dotenv

load_dotenv()

# Verify API key on startup
if not os.getenv("ANTHROPIC_API_KEY"):
    st.error("⚠️ ANTHROPIC_API_KEY not configured. Set it in Railway dashboard or environment.")
    st.stop()
```

---

## Update modules/report_generator.py

Change model to Opus:

```python
from config import CLAUDE_MODEL, CLAUDE_MAX_TOKENS

# In synthesize_with_claude function:
response = client.messages.create(
    model=CLAUDE_MODEL,  # Uses claude-opus-4-20250514 from config
    max_tokens=CLAUDE_MAX_TOKENS,
    ...
)
```

---

## Deployment Commands

After creating all files, user runs:

```bash
# Set API key
export ANTHROPIC_API_KEY=sk-ant-api03-xxxxx

# Full deploy
make full
```

Or step by step:

```bash
make setup    # Create config files
make deploy   # Deploy to Railway
make logs     # View logs
make open     # Open in browser
```

---

## File Checklist

After implementation, project should have:

```
o2c_assessment_app/
├── app.py                 (updated)
├── config.py              (updated)
├── requirements.txt
├── railway.json           (new)
├── Procfile               (new)
├── Makefile               (new)
├── deploy.sh              (new)
├── runtime.txt            (new)
├── .gitignore             (updated)
├── .streamlit/
│   └── config.toml        (new)
├── modules/
│   ├── report_generator.py (updated - Opus model)
│   └── ...
├── grid_layout.py
└── knowledge_base.json
```
