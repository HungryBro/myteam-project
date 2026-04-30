# Windows Setup Guide

This guide provides step-by-step instructions for setting up the OpenClaw Multi-Agent Trading Bot on a Windows environment.

## Prerequisites

Before you begin, ensure you have the following installed on your Windows PC:

1. **Docker Desktop**: Installed and configured to use WSL2.
2. **WSL2 (Windows Subsystem for Linux)**: Required for Docker Desktop.
3. **MetaTrader 5 (MT5)**: Installed (e.g., Markets4you terminal).
4. **Python 3.11+**: Installed on Windows (required for the MT5 Python Library).
5. **Git**: For cloning the repository.

## Step-by-Step Installation

### 1. Clone the Repository

Open your terminal (Command Prompt, PowerShell, or Git Bash) and clone the repository:

```bash
git clone https://github.com/HungryBro/myteam-project.git
cd myteam-project
```

### 2. Configure Environment Variables

Copy the example environment file to create your own `.env` file:

```bash
cp .env.example .env
```

### 3. Fill in the `.env` File

Open the `.env` file and fill in the required information across the 15 categories:

1. **OpenClaw Gateway**: Set your gateway token and root password.
2. **LLM API Keys (OpenRouter)**: 1 key per Agent (Chief, Analyst, Forex Exec, Crypto Exec).
3. **LLM for Services**: Key for YouTube Research and Summarization.
4. **Discord Bot Tokens**: 1 token per Agent.
5. **Discord Server & Channel IDs**: Your Discord server ID and specific channel IDs.
6. **MT5 (Forex)**: Your MT5 Login, Password, Server, and Path to `terminal64.exe`.
7. **Binance (Crypto)**: (Currently disabled) API Key and Secret.
8. **Telegram**: Bot Token and Chat ID for notifications.
9. **n8n**: Encryption Key, Password, Webhook Secret, and API Key.
10. **Google Workspace**: (Optional) Service account base64 string.
11. **Unified Trading MCP Server**: Host (`0.0.0.0`) and Port (`3003`).
12. **TradingView MCP**: URL (`http://tradingview-mcp:8000`).
13. **SearXNG**: URL (`http://searxng:8080`).
14. **Crawl4AI**: URL (`http://crawl4ai:8081`).
15. **YouTube Research Service**: OpenRouter Key and Model.

### 4. Start Docker Services

Run the following command to start all Docker containers (OpenClaw, n8n, SearXNG, Crawl4AI, Discord Bots, etc.):

```bash
make up
```

### 5. Start Unified Trading MCP Server

The Unified Trading MCP Server must run directly on Windows because the MT5 Python Library requires a Windows environment.

Open a **new terminal window** on Windows, navigate to the `services/trading-mcp` directory, install dependencies, and start the server:

```bash
cd services/trading-mcp
pip install -r requirements.txt
uvicorn server:app --host 0.0.0.0 --port 3003
```

*Keep this terminal window open.*

### 6. Open MT5 Terminal

Ensure your MetaTrader 5 terminal is open and logged into the correct account (as specified in your `.env` file). The terminal must remain open for the bot to execute trades.

### 7. Import n8n Workflows

1. Open your browser and navigate to your n8n instance (usually `http://localhost:5678`).
2. Go to **Workflows** -> **Add Workflow** -> **Import from File**.
3. Import all 14 JSON files located in the `n8n/workflows/` directory.
4. Activate the workflows.

### 8. Verify Discord Bots

Check your Discord server to ensure all 4 bots (Chief, Analyst, Forex Executor, Crypto Executor) are online and have the correct permissions in their respective channels.

## Testing Checklist

- [ ] Docker containers are running (`docker-compose ps`).
- [ ] Unified Trading MCP Server is running on port 3003.
- [ ] MT5 Terminal is open and connected.
- [ ] n8n workflows are imported and active.
- [ ] Discord bots are online.

## Troubleshooting

- **MT5 Connection Failed**: Ensure the MT5 terminal is open, Auto Trading is enabled, and the credentials in `.env` are correct.
- **Docker Services Not Starting**: Check if Docker Desktop is running and WSL2 is properly configured.
- **Discord Bots Offline**: Verify the bot tokens in `.env` and ensure the bots are invited to your server.
- **n8n Webhook Errors**: Check the `N8N_WEBHOOK_SECRET` and ensure the n8n container can communicate with the OpenClaw Gateway.
