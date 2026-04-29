# Confidence Score System

The Confidence Score is a quantitative measure used to evaluate the strength of a trading signal. It is calculated by the Analyst and used by the Chief to make decisions and by the Executors to determine position sizing.

## Scoring Components

| Component | Score Range | Description |
|---|---|---|
| **Base Score** | 4 | Starting point for any analyzed signal. |
| **TradingView TA** | 0 - 2 | Technical Analysis strength (Indicators, Patterns). |
| **YouTube Consensus** | 0 - 2 | Agreement among 3+ designated YouTube channels. |
| **Reddit Sentiment** | 0 - 1 | Overall sentiment from relevant subreddits. |
| **Backtest Results** | 0 - 1 | Historical performance of the strategy for the symbol. |
| **Trading Rules** | 0 - 2 | Alignment with THE WALLSTREET FINANCIAL rules. |
| **Total Score** | **Max 10** | Capped at 10. |

## Action Thresholds

| Total Score | Action | Position Size |
|---|---|---|
| **1 - 4** | **DO NOT TRADE** | 0% |
| **5 - 6** | **TRADE** | 5% of Equity |
| **7 - 8** | **TRADE** | 7% - 8% of Equity |
| **9 - 10** | **TRADE** | 10% of Equity |

## Rules for Scoring
- **YouTube Consensus:** If 3 or more designated YouTubers provide the same signal (BUY/SELL) within the last 24 hours, add 2 points.
- **TradingView Confirmation:** If TradingView technical analysis (e.g., `coin_analysis`) confirms the YouTube signal, ensure the TA score reflects this.
- **Capping:** The final score cannot exceed 10.
