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
