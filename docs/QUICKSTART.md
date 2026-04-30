# Quick Start Guide

Follow these 5 simple steps to get the OpenClaw Multi-Agent Trading Bot up and running quickly.

### 1. Clone & Configure

Clone the repository and set up your environment variables:

```bash
git clone https://github.com/HungryBro/myteam-project.git
cd myteam-project
cp .env.example .env
```
*Open `.env` and fill in your API keys, Discord tokens, and MT5 credentials.*

### 2. Start Docker Services

Launch the core infrastructure (OpenClaw, n8n, SearXNG, Crawl4AI, Discord Bots):

```bash
make up
```

### 3. Start MT5 & Trading MCP Server

1. Open your **MetaTrader 5** terminal on Windows.
2. Open a new Windows terminal, navigate to the `services/trading-mcp` folder, and start the Unified Trading MCP Server:

```bash
cd services/trading-mcp
pip install -r requirements.txt
uvicorn server:app --host 0.0.0.0 --port 3003
```

### 4. Import n8n Workflows

1. Open n8n in your browser (usually `http://localhost:5678`).
2. Import the 14 workflow JSON files from the `n8n/workflows/` directory.
3. Activate the workflows.

### 5. Test via Discord

Check your Discord server. The bots should be online. You can test the system by sending a message in the appropriate channel (e.g., asking the Analyst for a market update in `#company_reports`).
