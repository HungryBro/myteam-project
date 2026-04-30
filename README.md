# OpenClaw Multi-Agent Autonomous Trading Bot

> **หมายเหตุสำหรับผู้ใช้งานชาวไทย:** Repository นี้ถูกเขียนเอกสารหลักเป็นภาษาอังกฤษเพื่อให้เป็นมาตรฐานสากล แต่คุณสามารถอ่านโครงสร้างและการทำงานได้จากเอกสารต่างๆ ในโฟลเดอร์ `docs/`

An advanced, multi-agent autonomous trading system built on the OpenClaw framework. This bot integrates technical analysis, sentiment analysis, YouTube research, and automated execution across Forex and Crypto markets.

## 🏗️ Architecture

```text
┌─────────────────────────────────────────────────────────────────┐
│                        WINDOWS PC                                │
│                                                                   │
│  ┌─────────────────────┐    ┌──────────────────────────────────┐ │
│  │   MetaTrader 5       │    │   Docker Desktop (WSL2)          │ │
│  │   (Markets4you)      │    │                                  │ │
│  │                       │    │  ┌──────────┐ ┌──────────────┐  │ │
│  │   ← MT5 Python Lib → │    │  │ OpenClaw │ │ TradingView  │  │ │
│  │                       │    │  │ Gateway  │ │ MCP Server   │  │ │
│  └─────────────────────┘    │  └──────────┘ └──────────────┘  │ │
│           ↕                  │  ┌──────────┐ ┌──────────────┐  │ │
│  ┌─────────────────────┐    │  │   n8n    │ │   SearXNG    │  │ │
│  │  Unified Trading     │    │  │ (14 jobs)│ │   (Search)   │  │ │
│  │  MCP Server (FastAPI)│    │  └──────────┘ └──────────────┘  │ │
│  │  Port 3003           │    │  ┌──────────┐ ┌──────────────┐  │ │
│  │  ├─ MT5Adapter       │    │  │ Crawl4AI │ │ Discord Bots │  │ │
│  │  └─ BinanceAdapter   │    │  │ (Scrape) │ │ (4 bots)     │  │ │
│  │     (disabled)       │    │  └──────────┘ └──────────────┘  │ │
│  └─────────────────────┘    └──────────────────────────────────┘ │
│                                        │                          │
└────────────────────────────────────────┼──────────────────────────┘
                                         │
                    ┌────────────────────┼────────────────────┐
                    ▼                    ▼                    ▼
           ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
           │   Discord    │    │  OpenRouter  │    │   Binance    │
           │   Server     │    │  (LLM API)  │    │  (disabled)  │
           └──────────────┘    └──────────────┘    └──────────────┘
```

## 🤖 The 4 Agents

The system operates using a team of 4 specialized AI agents:

1. **Chief (Harper)**: The CEO. Coordinates the team, makes high-level decisions, and reviews daily/weekly performance.
2. **Analyst (Parker)**: The Researcher. Analyzes markets using TradingView MCP, summarizes YouTube insights, and calculates the Confidence Score.
3. **Forex Executor (Victor)**: The Trader. Executes trades on MetaTrader 5 based on Chief's decisions and manages positions.
4. **Crypto Executor (Disabled)**: Ready for future Binance integration.

For more details, see [docs/AGENTS.md](docs/AGENTS.md).

## ✨ Key Features

- **TradingView MCP Integration**: Access to 20+ tools including live prices, technical indicators, backtesting, and sentiment analysis.
- **YouTube Research**: Automated daily scanning of 7 top trading channels (e.g., The Wall Street Financial, DataDash, สาระสนเทรด).
- **n8n Automation**: 14 automated workflows managing everything from morning scans to weekend reviews.
- **Discord Integration**: 4 dedicated bots operating across 12 channels for real-time reporting and control.
- **Confidence Score System**: A robust 1-10 scoring system combining TA, YouTube consensus, Reddit sentiment, and backtest results.
- **Adaptive Trading Rules**: Based on Price Action and Support/Resistance principles from THE WALLSTREET FINANCIAL.

## 🛠️ Tech Stack

- **Core Framework**: OpenClaw (based on HungryBro/sempre)
- **Infrastructure**: Docker Desktop (WSL2) on Windows
- **Trading Execution**: MetaTrader 5 Python Library (Runs directly on Windows)
- **API Gateway**: FastAPI (Unified Trading MCP Server)
- **Automation**: n8n
- **Search & Scraping**: SearXNG, Crawl4AI
- **LLM Provider**: OpenRouter (GPT-4o-mini, etc.)
- **Communication**: Discord.py

## 📂 Repository Structure

```text
myteam-project/
├── README.md
├── docker-compose.yml
├── config.json
├── Makefile
├── .env.example
├── docs/
│   ├── SETUP-WINDOWS.md
│   ├── QUICKSTART.md
│   └── AGENTS.md
├── agents/
│   ├── chief/
│   ├── analyst/
│   ├── forex_executor/
│   └── crypto_executor/
├── memory/
│   ├── TRADING-RULES.md
│   └── CONFIDENCE-SCORE.md
├── km-vault/
├── skills/
├── tools/
├── services/
│   ├── discord/
│   ├── trading-mcp/
│   ├── tradingview-mcp/
│   ├── youtube-research/
│   ├── searxng/
│   └── crawl4ai/
└── n8n/
    └── workflows/ (14 JSON files)
```

## 🚀 Quick Start

For a fast setup, check out the [Quick Start Guide](docs/QUICKSTART.md).
For detailed installation instructions, see the [Windows Setup Guide](docs/SETUP-WINDOWS.md).

## 📜 Trading Rules & Confidence Score

The bot operates strictly based on predefined rules and a confidence scoring system:
- **Trading Rules**: Focuses on Price Action, Twin Candles, and Unused Levels. See [memory/TRADING-RULES.md](memory/TRADING-RULES.md).
- **Confidence Score**: Trades are only executed if the score is 5 or higher, with position sizing (5-10%) scaling with confidence. See [memory/CONFIDENCE-SCORE.md](memory/CONFIDENCE-SCORE.md).

## ⚙️ n8n Workflows

The system uses 14 automated workflows:

| Workflow | Schedule | Agent | Purpose |
| :--- | :--- | :--- | :--- |
| `01-youtube-morning-scan` | 07:00 Daily | Analyst | Scan YouTube for overnight updates |
| `02-morning-research` | 08:00 Daily | Analyst | Comprehensive morning market research |
| `03-crypto-trade-execution` | 09:00 Daily | Crypto Exec | Execute crypto trades (Currently Disabled) |
| `04-midday-scan` | 14:00 Daily | Analyst | Midday market check |
| `05-youtube-evening-scan` | 18:00 Daily | Analyst | Evening YouTube analysis |
| `06-daily-summary` | 20:00 Daily | Chief | End of day performance summary |
| `07-forex-asian-session` | 06:00 Mon-Fri | Forex Exec | Asian session trading |
| `08-forex-london-session` | 14:00 Mon-Fri | Forex Exec | London session trading |
| `09-forex-ny-session` | 19:00 Mon-Fri | Forex Exec | New York session trading |
| `10-forex-weekend-close` | 22:00 Fri | Forex Exec | Close positions before weekend |
| `11-weekly-review` | 21:00 Sun | Chief | Weekly performance review |
| `12-system-health-check` | Every 5 mins | System | Monitor system uptime |
| `13-openrouter-usage` | 23:00 Daily | System | Track API usage costs |
| `14-economic-calendar` | 06:00 Daily | Analyst | Check daily economic events |

## ⚠️ Disclaimer

**NOT FINANCIAL ADVICE.** This software is for educational and research purposes only. Trading in financial markets involves a high degree of risk. The creators and contributors of this repository are not responsible for any financial losses incurred while using this software. Use at your own risk.

## 📄 License

This project is licensed under the MIT License.
