# O2C AI Agent & MCP Readiness Assessment App

A Streamlit application that transforms static paper-based Order-to-Cash assessments into intelligent, AI-powered strategic roadmaps for AI Agent and MCP (Model Context Protocol) adoption.

## Features

- **AI Vision Score Extraction**: Upload an image of your completed assessment and automatically extract Importance/Readiness scores using Claude Vision
- **Intelligent Analysis**: Categorizes capabilities into priority buckets (Urgent Gap, Critical Gap, Strength, etc.)
- **Strategic Reports**: Generates comprehensive strategic priority guides using Claude AI
- **Agent & MCP Mapping**: Maps each capability to specific Zuora AI agents and MCP tools
- **Export Options**: Download reports as DOCX, PDF, or Markdown

## Project Structure

```
o2c_assessment_app/
├── app.py                      # Main Streamlit application
├── config.py                   # Configuration settings
├── knowledge_base.json         # Complete capability knowledge base (45 capabilities, 8 phases)
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
├── modules/
│   ├── __init__.py
│   ├── image_processor.py      # Claude Vision score extraction
│   ├── score_analyzer.py       # Priority analysis engine
│   ├── report_generator.py     # LLM report generation
│   └── export_handler.py       # DOCX/PDF export
└── templates/
    └── styles.css              # Custom styling
```

## Setup Instructions

### 1. Prerequisites

- Python 3.9 or higher
- An Anthropic API key (get one at https://console.anthropic.com/)

### 2. Installation

```bash
# Clone or navigate to the project directory
cd o2c_assessment_app

# Create a virtual environment (recommended)
python -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your Anthropic API key
# ANTHROPIC_API_KEY=your_api_key_here
```

### 4. Run the Application

```bash
streamlit run app.py
```

The app will open in your default web browser at `http://localhost:8501`

## Usage

### Step 1: Upload Assessment Image

1. Take a photo or scan of your completed Recurring Revenue Management Lifecycle Assessment
2. Upload the image using the file uploader in the app
3. The app will use Claude Vision to automatically extract Importance (I) and Readiness (R) scores

### Step 2: Review & Edit Scores

1. Review the extracted scores in the expandable sections
2. Edit any scores that were incorrectly extracted
3. Ensure all 45 capabilities have appropriate I/R scores

### Step 3: Configure Context

Use the sidebar to provide:
- Company/Customer Name
- Industry
- Primary Business Model
- Priority Focus Areas

### Step 4: Generate Report

1. Click "Generate Strategic Report"
2. Wait for the AI to analyze capabilities and generate the comprehensive report
3. Review the Priority Matrix Overview showing distribution across categories

### Step 5: Export Report

Download the report in your preferred format:
- **DOCX**: For further editing in Microsoft Word
- **PDF**: For sharing and presentations
- **Markdown**: For version control and technical documentation

## Report Contents

The generated strategic report includes:

1. **Executive Summary**: Overall readiness assessment and top priorities
2. **Priority Matrix Analysis**: Distribution across priority categories
3. **Urgent Gaps Detail**: Deep dive into high-importance, low-readiness capabilities
4. **Strengths to Protect**: What's working well and how to maintain it
5. **Phase-by-Phase Recommendations**: Analysis across all 8 O2C phases
6. **AI Agent Roadmap**: Timeline for agent deployment (NOW/NEAR/LATER)
7. **MCP Integration Plan**: Developer MCP, Remote MCP Server, and MCP Gateway strategy
8. **Implementation Timeline**: 30/60/90 day plan with milestones
9. **Next Steps**: Immediate actions and success metrics

## 8 O2C Phases Covered

1. **Configure and Price**: AI-optimized monetization
2. **Quote and Sell**: Agentic, omnichannel quoting
3. **Invoice**: Self-healing billing flows
4. **Collect**: Autonomous payment recovery
5. **Provision**: Instant access & entitlement
6. **Recognize and Report**: Automated compliance summaries
7. **Learn**: Closed-loop intelligence
8. **Sustain and Grow**: Proactive retention & expansion

## AI Agents & MCP Tools

The knowledge base includes mappings to:

**Concierge Agents:**
- Anantha Concierge
- Zuora AI Concierge

**Business Agents:**
- Billing Operations Agent
- Collections Manager Agent
- Revenue Accountant Agent
- Customer Health Agent
- Churn Agent
- Quote Agent / Deal Assist
- And more...

**MCP Tools:**
- Catalog management
- Pricing configuration
- Order orchestration
- Usage/entitlement enforcement
- Revenue recognition workflows
- And more...

## Troubleshooting

### Issue: API Key Error
**Solution**: Ensure your `.env` file contains a valid `ANTHROPIC_API_KEY`

### Issue: Image Extraction Quality
**Solution**:
- Use high-resolution images with good lighting
- Ensure handwriting is clear and legible
- Review and edit scores after extraction

### Issue: PDF Export Fails
**Solution**: Install WeasyPrint dependencies:
```bash
# macOS
brew install cairo pango gdk-pixbuf libffi

# Ubuntu/Debian
sudo apt-get install build-essential python3-dev python3-pip python3-setuptools python3-wheel python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info

# Windows: Use pre-built wheels
pip install --upgrade weasyprint
```

## Development

### Running Tests
```bash
pytest tests/
```

### Code Structure

- **config.py**: Centralized configuration with thresholds and paths
- **image_processor.py**: Claude Vision API integration for score extraction
- **score_analyzer.py**: Priority categorization logic (Urgent Gap, Strength, etc.)
- **report_generator.py**: Claude API integration for strategic report generation
- **export_handler.py**: DOCX/PDF/Markdown export functionality

## Technology Stack

- **Streamlit**: Web application framework
- **Anthropic Claude**: Vision and text generation API
- **python-docx**: DOCX export
- **WeasyPrint**: PDF export
- **Pillow**: Image processing

## License

This project is built for internal use and assessment purposes.

## Support

For questions or issues, please refer to:
- `CLAUDE.md`: Build instructions and key notes
- `spec.md`: Complete technical specification

---

Built with Claude Code CLI
