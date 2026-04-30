
#!/usr/bin/env python3
"""
CLI wrapper for tradingview-mcp — called by OpenClaw agent via bash.

Usage:
    python3 trading.py price AAPL
    python3 trading.py snapshot
    python3 trading.py backtest AAPL rsi 1y
    python3 trading.py backtest BTC-USD bollinger 6mo 1h
    python3 trading.py compare AAPL 2y
    python3 trading.py walkforward AAPL rsi 2y
    python3 trading.py sentiment BTC
    python3 trading.py top_gainers KUCOIN 15m 25
    python3 trading.py top_losers KUCOIN 15m 25
    python3 trading.py bollinger_scan KUCOIN 4h 0.04 50
    python3 trading.py rating_filter KUCOIN 5m 2 25
    python3 trading.py coin_analysis BTCUSDT KUCOIN 15m
    python3 trading.py consecutive_candles KUCOIN bullish 3 15m 20
    python3 trading.py candle_pattern KUCOIN 15m 3 10.0 15
    python3 trading.py volume_breakout KUCOIN 15m 2.0 3.0 25
    python3 trading.py volume_confirm BTCUSDT KUCOIN 15m
    python3 trading.py smart_volume KUCOIN 2.0 2.0 any 20
    python3 trading.py multi_agent BTCUSDT KUCOIN 15m
    python3 trading.py multi_timeframe BTCUSDT KUCOIN
    python3 trading.py news crypto 10
    python3 trading.py combined BTCUSDT KUCOIN 15m
    python3 trading.py screener_bullish NASDAQ
    python3 trading.py screener_oversold NASDAQ

Install path: ~/.openclaw/tools/trading.py
"""
import sys
import json
import os

# Auto-discover site-packages for tradingview-mcp-server
SITE_PACKAGES = "/root/.local/share/uv/tools/tradingview-mcp-server/lib/python3.12/site-packages"
if os.path.exists(SITE_PACKAGES):
    sys.path.insert(0, SITE_PACKAGES)
else:
    # Fallback: search common uv paths
    import glob
    candidates = glob.glob(
        os.path.expanduser(
            "~/.local/share/uv/tools/tradingview-mcp-server/lib/python*/site-packages"
        )
    )
    if candidates:
        sys.path.insert(0, candidates[0])

try:
    from tradingview_mcp.core.services.yahoo_finance_service import get_price, get_market_snapshot
    from tradingview_mcp.core.services.backtest_service import run_backtest, compare_strategies, walk_forward_backtest
    from tradingview_mcp.core.services.sentiment_service import analyze_sentiment
    from tradingview_mcp.core.services.screener_service import (
        fetch_bollinger_analysis,
        fetch_trending_analysis,
        analyze_coin,
        scan_consecutive_candles,
        scan_advanced_candle_patterns_single_tf,
        fetch_multi_timeframe_patterns,
        run_multi_timeframe_analysis,
    )
    from tradingview_mcp.core.services.scanner_service import (
        volume_breakout_scan,
        volume_confirmation_analyze,
        smart_volume_scan,
    )
    from tradingview_mcp.core.services.multi_agent_service import run_multi_agent_analysis
    from tradingview_mcp.core.services.news_service import fetch_news_summary
    from tradingview_mcp.core.utils.validators import (
        sanitize_timeframe,
        sanitize_exchange,
    )
except ImportError as e:
    print(json.dumps({"error": str(e), "fix": "Run: uv tool install tradingview-mcp-server"}))
    sys.exit(1)

cmd = sys.argv[1] if len(sys.argv) > 1 else "help"
args = sys.argv[2:]

try:
    if cmd == "price":
        print(json.dumps(get_price(args[0]), indent=2))

    elif cmd == "snapshot":
        print(json.dumps(get_market_snapshot(), indent=2))

    elif cmd == "backtest":
        symbol   = args[0]
        strategy = args[1] if len(args) > 1 else "rsi"
        period   = args[2] if len(args) > 2 else "1y"
        interval = args[3] if len(args) > 3 else "1d"
        print(json.dumps(run_backtest(symbol, strategy, period, interval=interval), indent=2))

    elif cmd == "compare":
        symbol = args[0]
        period = args[1] if len(args) > 1 else "1y"
        print(json.dumps(compare_strategies(symbol, period), indent=2))

    elif cmd == "walkforward":
        symbol   = args[0]
        strategy = args[1] if len(args) > 1 else "rsi"
        period   = args[2] if len(args) > 2 else "2y"
        print(json.dumps(walk_forward_backtest(symbol, strategy, period), indent=2))

    elif cmd == "sentiment":
        print(json.dumps(analyze_sentiment(args[0]), indent=2))

    elif cmd == "top_gainers":
        exchange = args[0]
        timeframe = args[1] if len(args) > 1 else "15m"
        limit = int(args[2]) if len(args) > 2 else 25
        rows = fetch_trending_analysis(exchange, timeframe=timeframe, limit=limit)
        print(json.dumps([{"symbol": r["symbol"], "changePercent": r["changePercent"], "indicators": dict(r["indicators"])} for r in rows], indent=2))

    elif cmd == "top_losers":
        exchange = args[0]
        timeframe = args[1] if len(args) > 1 else "15m"
        limit = int(args[2]) if len(args) > 2 else 25
        rows = fetch_trending_analysis(exchange, timeframe=timeframe, limit=limit)
        rows.sort(key=lambda x: x["changePercent"])
        print(json.dumps([{"symbol": r["symbol"], "changePercent": r["changePercent"], "indicators": dict(r["indicators"])} for r in rows[:limit]], indent=2))

    elif cmd == "bollinger_scan":
        exchange = args[0]
        timeframe = args[1] if len(args) > 1 else "4h"
        bbw_threshold = float(args[2]) if len(args) > 2 else 0.04
        limit = int(args[3]) if len(args) > 3 else 50
        rows = fetch_bollinger_analysis(exchange, timeframe=timeframe, bbw_filter=bbw_threshold, limit=limit)
        print(json.dumps([{"symbol": r["symbol"], "changePercent": r["changePercent"], "indicators": dict(r["indicators"])} for r in rows], indent=2))

    elif cmd == "rating_filter":
        exchange = args[0]
        timeframe = args[1] if len(args) > 1 else "5m"
        rating = int(args[2]) if len(args) > 2 else 2
        limit = int(args[3]) if len(args) > 3 else 25
        rows = fetch_trending_analysis(exchange, timeframe=timeframe, filter_type="rating", rating_filter=rating, limit=limit)
        print(json.dumps([{"symbol": r["symbol"], "changePercent": r["changePercent"], "indicators": dict(r["indicators"])} for r in rows], indent=2))

    elif cmd == "coin_analysis":
        symbol = args[0]
        exchange = args[1] if len(args) > 1 else "KUCOIN"
        timeframe = args[2] if len(args) > 2 else "15m"
        print(json.dumps(analyze_coin(symbol, exchange, timeframe), indent=2))

    elif cmd == "consecutive_candles":
        exchange = args[0]
        pattern_type = args[1] if len(args) > 1 else "bullish"
        candle_count = int(args[2]) if len(args) > 2 else 3
        timeframe = args[3] if len(args) > 3 else "15m"
        limit = int(args[4]) if len(args) > 4 else 20
        print(json.dumps(scan_consecutive_candles(exchange, timeframe, pattern_type, candle_count, 2.0, limit), indent=2))

    elif cmd == "candle_pattern":
        exchange = args[0]
        base_timeframe = args[1] if len(args) > 1 else "15m"
        pattern_length = int(args[2]) if len(args) > 2 else 3
        min_size_increase = float(args[3]) if len(args) > 3 else 10.0
        limit = int(args[4]) if len(args) > 4 else 15
        print(json.dumps(scan_advanced_candle_patterns_single_tf(exchange, [], base_timeframe, pattern_length, min_size_increase, limit), indent=2))

    elif cmd == "volume_breakout":
        exchange = args[0]
        timeframe = args[1] if len(args) > 1 else "15m"
        volume_multiplier = float(args[2]) if len(args) > 2 else 2.0
        price_change_min = float(args[3]) if len(args) > 3 else 3.0
        limit = int(args[4]) if len(args) > 4 else 25
        print(json.dumps(volume_breakout_scan(exchange, timeframe, volume_multiplier, price_change_min, limit), indent=2))

    elif cmd == "volume_confirm":
        symbol = args[0]
        exchange = args[1] if len(args) > 1 else "KUCOIN"
        timeframe = args[2] if len(args) > 2 else "15m"
        print(json.dumps(volume_confirmation_analyze(symbol, exchange, timeframe), indent=2))

    elif cmd == "smart_volume":
        exchange = args[0]
        min_volume_ratio = float(args[1]) if len(args) > 1 else 2.0
        min_price_change = float(args[2]) if len(args) > 2 else 2.0
        rsi_range = args[3] if len(args) > 3 else "any"
        limit = int(args[4]) if len(args) > 4 else 20
        print(json.dumps(smart_volume_scan(exchange, min_volume_ratio, min_price_change, rsi_range, limit), indent=2))

    elif cmd == "multi_agent":
        symbol = args[0]
        exchange = args[1] if len(args) > 1 else "KUCOIN"
        timeframe = args[2] if len(args) > 2 else "15m"
        full_symbol = symbol.upper() if ":" in symbol else f"{exchange.upper()}:{symbol.upper()}"
        print(json.dumps(run_multi_agent_analysis(full_symbol, exchange, timeframe), indent=2))

    elif cmd == "multi_timeframe":
        symbol = args[0]
        exchange = args[1] if len(args) > 1 else "KUCOIN"
        full_symbol = symbol.upper() if ":" in symbol else f"{exchange.upper()}:{symbol.upper()}"
        print(json.dumps(run_multi_timeframe_analysis(full_symbol, exchange), indent=2))

    elif cmd == "news":
        symbol = args[0] if len(args) > 0 else None
        category = args[1] if len(args) > 1 else "stocks"
        limit = int(args[2]) if len(args) > 2 else 10
        print(json.dumps(fetch_news_summary(symbol, category, limit), indent=2))

    elif cmd == "combined":
        symbol = args[0]
        exchange = args[1] if len(args) > 1 else "NASDAQ"
        timeframe = args[2] if len(args) > 2 else "1D"
        tech = analyze_coin(symbol, exchange, timeframe)
        cat = "crypto" if exchange.upper() in ["BINANCE", "KUCOIN", "BYBIT", "MEXC"] else "stocks"
        sentiment = analyze_sentiment(symbol, category=cat)
        news = fetch_news_summary(symbol, category=cat, limit=5)
        tech_momentum = tech.get("market_sentiment", {}).get("momentum", "") if isinstance(tech, dict) else ""
        tech_bullish = tech_momentum == "Bullish"
        sent_bullish = sentiment.get("sentiment_score", 0) > 0.1
        signals_agree = tech_bullish == sent_bullish
        confidence = "HIGH" if signals_agree else "MIXED"
        tech_signal = tech.get("market_sentiment", {}).get("buy_sell_signal", "N/A") if isinstance(tech, dict) else "N/A"
        print(json.dumps({
            "symbol": symbol,
            "exchange": exchange,
            "timeframe": timeframe,
            "technical": tech,
            "sentiment": sentiment,
            "news": {"count": news.get("count", 0), "latest": news.get("items", [])[:3]},
            "confluence": {
                "signals_agree": signals_agree,
                "confidence": confidence,
                "recommendation": (
                    f"Technical {tech_signal} "
                    f"{'confirmed by' if signals_agree else 'conflicts with'} "
                    f"{sentiment.get('sentiment_label', 'Neutral')} Reddit sentiment "
                    f"({sentiment.get('posts_analyzed', 0)} posts analyzed)"
                ),
            },
        }, indent=2))

    elif cmd == "screener_bullish":
        exchange = args[0]
        # This function is not directly available in server.py as a single call. Need to simulate.
        # For now, I'll use top_gainers as a proxy, as it's the closest available.
        timeframe = args[1] if len(args) > 1 else "1D"
        limit = int(args[2]) if len(args) > 2 else 25
        rows = fetch_trending_analysis(exchange, timeframe=timeframe, limit=limit)
        print(json.dumps([{"symbol": r["symbol"], "changePercent": r["changePercent"], "indicators": dict(r["indicators"])} for r in rows], indent=2))

    elif cmd == "screener_oversold":
        exchange = args[0]
        # This function is not directly available in server.py as a single call. Need to simulate.
        # For now, I'll use top_losers as a proxy, as it's the closest available.
        timeframe = args[1] if len(args) > 1 else "1D"
        limit = int(args[2]) if len(args) > 2 else 25
        rows = fetch_trending_analysis(exchange, timeframe=timeframe, limit=limit)
        rows.sort(key=lambda x: x["changePercent"])
        print(json.dumps([{"symbol": r["symbol"], "changePercent": r["changePercent"], "indicators": dict(r["indicators"])} for r in rows[:limit]], indent=2))

    elif cmd == "help":
        print("Commands: price <sym> | snapshot | backtest <sym> <strategy> <period> [interval] | compare <sym> [period] | walkforward <sym> [strategy] [period] | sentiment <sym> | top_gainers <exchange> [timeframe] [limit] | top_losers <exchange> [timeframe] [limit] | bollinger_scan <exchange> [timeframe] [threshold] [limit] | rating_filter <exchange> [timeframe] [rating] [limit] | coin_analysis <symbol> <exchange> [timeframe] | consecutive_candles <exchange> [direction] [min_count] [timeframe] [limit] | candle_pattern <exchange> [timeframe] [pattern_length] [min_size_increase] [limit] | volume_breakout <exchange> [timeframe] [volume_multiplier] [price_change_min] [limit] | volume_confirm <symbol> <exchange> [timeframe] | smart_volume <exchange> [min_volume_ratio] [min_price_change] [rsi_range] [limit] | multi_agent <symbol> <exchange> [timeframe] | multi_timeframe <symbol> <exchange> | news [symbol] [category] [limit] | combined <symbol> <exchange> [timeframe] | screener_bullish <exchange> [timeframe] [limit] | screener_oversold <exchange> [timeframe] [limit]")
        print("Strategies: rsi | bollinger | macd | ema_cross | supertrend | donchian")

    else:
        print(json.dumps({"error": f"Unknown command: {cmd}"}))

except Exception as e:
    print(json.dumps({"error": str(e)}))
