# Unified Trading MCP Server

This service provides a unified interface for interacting with different trading brokers, currently supporting MetaTrader5 (Forex) and Binance (Crypto).

## Features

- **Unified API:** A single HTTP API to interact with multiple brokers.
- **MetaTrader5 Adapter:** Connects to MetaTrader5 terminals for Forex trading.
- **Binance Adapter:** (Disabled by default) Connects to Binance for cryptocurrency trading.
- **FastAPI:** High-performance web framework for the HTTP server.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/HungryBro/myteam-project.git
    cd myteam-project/services/trading-mcp
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment Variables:**
    Create a `.env` file in the root of the `myteam-project` directory (or update `.env.example`) with the following variables:

    ```
    MT5_LOGIN=your_mt5_login
    MT5_PASSWORD=your_mt5_password
    MT5_SERVER=your_mt5_server_name # e.g., Markets4you-Cent
    MT5_PATH=C:\Program Files\MetaTrader 5\terminal64.exe # Path to your MT5 terminal on Windows

    BINANCE_API_KEY=your_binance_api_key
    BINANCE_API_SECRET=your_binance_api_secret

    TRADING_MCP_PORT=3003
    ```

    **Note:** The `MT5_PATH` is crucial as the MT5 Python library needs to access the MT5 terminal running on Windows. This server is intended to run directly on a Windows machine, not in Docker, due to MT5's requirements.

## Usage

1.  **Run the server:**
    ```bash
    uvicorn server:app --host 0.0.0.0 --port 3003
    ```

    The server will be accessible at `http://localhost:3003` (or `http://host.docker.internal:3003` from within Docker containers).

2.  **API Endpoints:**

    All endpoints return JSON.

    -   **GET /api/v1/{broker}/account**
        Get account balance and margin information.
        `broker`: `forex` or `binance`

    -   **GET /api/v1/{broker}/positions**
        Get currently open positions.
        `broker`: `forex` or `binance`

    -   **GET /api/v1/{broker}/ticker/{symbol}**
        Get current price for a symbol.
        `broker`: `forex` or `binance`
        `symbol`: Trading symbol (e.g., `XAUUSD` for Forex, `BTCUSDT` for Binance)

    -   **POST /api/v1/{broker}/order**
        Place a new order.
        `broker`: `forex` or `binance`
        Body: `{"symbol": "XAUUSD", "side": "buy", "type": "market", "qty": 0.01, "price": null, "sl": null, "tp": null, "comment": "My order"}`

    -   **PUT /api/v1/{broker}/order/{order_id}**
        Modify an existing order (e.g., stop loss, take profit).
        `broker`: `forex` or `binance`
        `order_id`: The ID of the order to modify
        Body: `{"stop_loss": 1.2345, "take_profit": 1.2500}`

    -   **DELETE /api/v1/{broker}/order/{order_id}**
        Cancel an open order.
        `broker`: `forex` or `binance`
        `order_id`: The ID of the order to cancel

    -   **GET /api/v1/{broker}/orders?symbol={symbol}**
        Get pending orders. Optional `symbol` query parameter.
        `broker`: `forex` or `binance`

    -   **GET /api/v1/{broker}/trade_history?days={days}**
        Get trade history. Optional `days` query parameter to specify the number of past days.
        `broker`: `forex` or `binance`

## Binance Adapter Status

The Binance adapter is **disabled by default**. If you attempt to call a Binance endpoint without configuring `BINANCE_API_KEY` and `BINANCE_API_SECRET` in your environment variables, the server will return an error: `"Binance disabled — please configure API key"`.
