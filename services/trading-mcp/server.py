
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

# Import adapters (will be created next)
from .mt5_adapter import MT5Adapter
from .binance_adapter import BinanceAdapter

app = FastAPI()

# Placeholder for adapters
import os

mt5_login = os.getenv("MT5_LOGIN")
mt5_password = os.getenv("MT5_PASSWORD")
mt5_server = os.getenv("MT5_SERVER")
mt5_path = os.getenv("MT5_PATH")

binance_api_key = os.getenv("BINANCE_API_KEY")
binance_api_secret = os.getenv("BINANCE_API_SECRET")

# Initialize adapters
mt5_adapter = MT5Adapter(login=mt5_login, password=mt5_password, server=mt5_server, path=mt5_path)
binance_enabled = False # Binance disabled by default
if binance_api_key and binance_api_secret:
    binance_enabled = True
binance_adapter = BinanceAdapter(api_key=binance_api_key, api_secret=binance_api_secret, enabled=binance_enabled)




def get_adapter(broker: str):
    if broker == "forex":
        return mt5_adapter
    elif broker == "binance":
        return binance_adapter
    else:
        raise HTTPException(status_code=404, detail="Broker not found")


class PlaceOrderRequest(BaseModel):
    symbol: str
    side: str
    type: str
    qty: float
    price: Optional[float] = None
    sl: Optional[float] = None
    tp: Optional[float] = None
    comment: Optional[str] = None

class ModifyOrderRequest(BaseModel):
    order_id: str
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None

@app.get("/api/v1/{broker}/account")
async def get_account_info(broker: str):
    adapter = get_adapter(broker)
    return adapter.get_account(broker)

@app.get("/api/v1/{broker}/positions")
async def get_open_positions(broker: str):
    adapter = get_adapter(broker)
    return adapter.get_positions(broker)

@app.get("/api/v1/{broker}/ticker/{symbol}")
async def get_symbol_ticker(broker: str, symbol: str):
    adapter = get_adapter(broker)
    return adapter.get_ticker(broker, symbol)

@app.post("/api/v1/{broker}/order")
async def place_new_order(broker: str, request: PlaceOrderRequest):
    adapter = get_adapter(broker)
    return adapter.place_order(broker, **request.dict())

@app.put("/api/v1/{broker}/order/{order_id}")
async def modify_existing_order(broker: str, order_id: str, request: ModifyOrderRequest):
    adapter = get_adapter(broker)
    return adapter.modify_order(broker, order_id, **request.dict())

@app.delete("/api/v1/{broker}/order/{order_id}")
async def cancel_existing_order(broker: str, order_id: str):
    adapter = get_adapter(broker)
    return adapter.cancel_order(broker, order_id)

@app.get("/api/v1/{broker}/orders")
async def get_pending_orders(broker: str, symbol: Optional[str] = None):
    adapter = get_adapter(broker)
    return adapter.get_open_orders(broker, symbol)

@app.get("/api/v1/{broker}/trade_history")
async def get_trade_history_data(broker: str, days: Optional[int] = None):
    adapter = get_adapter(broker)
    return adapter.get_trade_history(broker, days)
