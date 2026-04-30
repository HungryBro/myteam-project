
import MetaTrader5 as mt5
from fastapi import HTTPException

class MT5Adapter:
    def __init__(self, login, password, server, path):
        if not mt5.initialize(path=path):
            raise HTTPException(status_code=500, detail=f"MT5 initialization failed: {mt5.last_error()}")
        if not mt5.login(login=login, password=password, server=server):
            raise HTTPException(status_code=500, detail=f"MT5 login failed: {mt5.last_error()}")
        print("MT5 Adapter initialized and logged in.")

    def get_account(self, broker):
        account_info = mt5.account_info()
        if account_info is None:
            raise HTTPException(status_code=500, detail=f"Failed to get account info: {mt5.last_error()}")
        return {
            "broker": broker,
            "balance": account_info.balance,
            "equity": account_info.equity,
            "margin": account_info.margin,
            "free_margin": account_info.margin_free,
            "currency": account_info.currency
        }

    def get_positions(self, broker):
        positions = mt5.positions_get()
        if positions is None:
            raise HTTPException(status_code=500, detail=f"Failed to get positions: {mt5.last_error()}")
        return [
            {
                "ticket": pos.ticket,
                "symbol": pos.symbol,
                "type": "buy" if pos.type == mt5.ORDER_TYPE_BUY else "sell",
                "volume": pos.volume,
                "price_open": pos.price_open,
                "current_price": pos.price_current,
                "profit": pos.profit,
                "time": pos.time
            } for pos in positions
        ]

    def get_ticker(self, broker, symbol):
        symbol_info = mt5.symbol_info_tick(symbol)
        if symbol_info is None:
            raise HTTPException(status_code=500, detail=f"Failed to get ticker for {symbol}: {mt5.last_error()}")
        return {
            "broker": broker,
            "symbol": symbol,
            "bid": symbol_info.bid,
            "ask": symbol_info.ask,
            "last": symbol_info.last,
            "time": symbol_info.time
        }

    def place_order(self, broker, symbol, side, type, qty, price=None, sl=None, tp=None, comment=None):
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": float(qty),
            "type": mt5.ORDER_TYPE_BUY if side == "buy" else mt5.ORDER_TYPE_SELL,
            "price": price if price else mt5.symbol_info_tick(symbol).ask if side == "buy" else mt5.symbol_info_tick(symbol).bid,
            "deviation": 20, # Slippage in points
            "magic": 202306,
            "comment": comment if comment else "Python script order",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        if sl is not None:
            request["sl"] = float(sl)
        if tp is not None:
            request["tp"] = float(tp)

        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            raise HTTPException(status_code=500, detail=f"Order placement failed: {result.comment} (retcode: {result.retcode})")
        return {"broker": broker, "order_id": result.order, "status": "placed", "comment": result.comment}

    def modify_order(self, broker, order_id, stop_loss=None, take_profit=None):
        request = {
            "action": mt5.TRADE_ACTION_SLTP,
            "order": int(order_id),
            "sl": float(stop_loss) if stop_loss is not None else 0.0,
            "tp": float(take_profit) if take_profit is not None else 0.0,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            raise HTTPException(status_code=500, detail=f"Order modification failed: {result.comment} (retcode: {result.retcode})")
        return {"broker": broker, "order_id": order_id, "status": "modified", "comment": result.comment}

    def cancel_order(self, broker, order_id):
        request = {
            "action": mt5.TRADE_ACTION_REMOVE,
            "order": int(order_id),
            "comment": "Cancel order",
        }
        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            raise HTTPException(status_code=500, detail=f"Order cancellation failed: {result.comment} (retcode: {result.retcode})")
        return {"broker": broker, "order_id": order_id, "status": "cancelled", "comment": result.comment}

    def get_open_orders(self, broker, symbol=None):
        orders = mt5.orders_get(symbol=symbol) if symbol else mt5.orders_get()
        if orders is None:
            raise HTTPException(status_code=500, detail=f"Failed to get open orders: {mt5.last_error()}")
        return [
            {
                "ticket": order.ticket,
                "symbol": order.symbol,
                "type": order.type,
                "state": order.state,
                "volume": order.volume_initial,
                "price_open": order.price_open,
                "current_price": order.price_current,
                "time_setup": order.time_setup
            } for order in orders
        ]

    def get_trade_history(self, broker, days=None):
        import datetime
        today = datetime.date.today()
        if days:
            date_from = today - datetime.timedelta(days=days)
        else:
            date_from = datetime.date(1970, 1, 1) # Get all history if days not specified

        history_orders = mt5.history_orders_get(date_from, today)
        if history_orders is None:
            raise HTTPException(status_code=500, detail=f"Failed to get trade history: {mt5.last_error()}")
        return [
            {
                "ticket": order.ticket,
                "symbol": order.symbol,
                "type": order.type,
                "state": order.state,
                "volume": order.volume_initial,
                "price_open": order.price_open,
                "price_current": order.price_current,
                "time_setup": order.time_setup,
                "time_done": order.time_done,
                "profit": order.profit
            } for order in history_orders
        ]
