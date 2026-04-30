# Agents Overview

The OpenClaw Multi-Agent Trading Bot operates using a team of 4 specialized AI agents. Each agent has a distinct role, specific tool permissions, and designated communication channels.

## 1. Chief (Harper)
- **Role**: Chief Executive Officer (CEO)
- **Responsibilities**: Oversees overall strategy, coordinates the other agents, makes high-level trading decisions based on Analyst reports, and conducts daily/weekly performance reviews.
- **Status**: Active

## 2. Analyst (Parker)
- **Role**: Market Analyst & Researcher
- **Responsibilities**: Conducts market research, performs technical analysis using TradingView MCP, summarizes insights from YouTube trading channels, and calculates the Confidence Score for potential trades.
- **Status**: Active

## 3. Forex Executor (Victor)
- **Role**: Forex Trading Executor
- **Responsibilities**: Executes Forex trades on MetaTrader 5 based on the Chief's decisions, manages open positions, and monitors risk.
- **Status**: Active

## 4. Crypto Executor
- **Role**: Crypto Trading Executor
- **Responsibilities**: Executes Crypto trades on Binance and manages crypto positions.
- **Status**: Disabled (Ready for future use)

---

## Agent × Tools Permission Matrix

| Tool / Service | Chief | Analyst | Forex Executor | Crypto Executor |
| :--- | :---: | :---: | :---: | :---: |
| **TradingView MCP** | ❌ | ✅ | ❌ | ❌ |
| **YouTube Research** | ❌ | ✅ | ❌ | ❌ |
| **SearXNG (Web Search)** | ✅ | ✅ | ❌ | ❌ |
| **Crawl4AI (Web Scrape)** | ✅ | ✅ | ❌ | ❌ |
| **MT5 Trading (Forex)** | ❌ | ❌ | ✅ | ❌ |
| **Binance Trading (Crypto)** | ❌ | ❌ | ❌ | ✅ |
| **File System (KM Vault)** | ✅ | ✅ | ✅ | ✅ |

---

## Discord Channel Permissions

The agents communicate and report their activities in specific Discord channels.

| Channel | Chief | Analyst | Forex Executor | Crypto Executor | Purpose |
| :--- | :---: | :---: | :---: | :---: | :--- |
| `#ceo_office` | ✅ | ❌ | ❌ | ❌ | High-level decisions, strategy |
| `#company_reports` | ✅ | ✅ | ❌ | ❌ | Research reports, daily summaries |
| `#trading_terminal` | ✅ | ✅ | ✅ | ✅ | General trading discussions |
| `#forex_trades` | ❌ | ❌ | ✅ | ❌ | Forex trade execution logs |
| `#crypto_trades` | ❌ | ❌ | ❌ | ✅ | Crypto trade execution logs |
| `#economic_calendar` | ❌ | ✅ | ❌ | ❌ | Economic events and news |
| `#agent_coworking` | ✅ | ✅ | ✅ | ✅ | Inter-agent communication |
