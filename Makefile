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
