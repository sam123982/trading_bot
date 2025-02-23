import pandas as pd
from indicators import calculate_ema, calculate_vwap, calculate_atr

def check_trade_signal(data: pd.DataFrame) -> str:
    """
    Determines if we should enter a CALL (BUY) or PUT (SELL) trade.
    
    Conditions:
    - Buy CALL: Price above VWAP & EMA(9) > EMA(21)
    - Buy PUT: Price below VWAP & EMA(9) < EMA(21)
    
    :param data: DataFrame containing market data (with 'close', 'high', 'low', 'volume')
    :return: 'CALL' for bullish trade, 'PUT' for bearish trade, or 'NO_TRADE'
    """
    data["EMA_9"] = calculate_ema(data, 9)
    data["EMA_21"] = calculate_ema(data, 21)
    data["VWAP"] = calculate_vwap(data)

    latest = data.iloc[-1]  # Get the latest candle

    if latest["close"] > latest["VWAP"] and latest["EMA_9"] > latest["EMA_21"]:
        return "CALL"
    elif latest["close"] < latest["VWAP"] and latest["EMA_9"] < latest["EMA_21"]:
        return "PUT"
    else:
        return "NO_TRADE"

def calculate_sl_tp(data: pd.DataFrame) -> tuple:
    """
    Calculate Stop-Loss (SL) and Take-Profit (TP) using ATR.
    
    - SL: Entry Price - (0.5 × ATR) for CALL, Entry Price + (0.5 × ATR) for PUT
    - TP: Entry Price + (0.5 × ATR) for CALL, Entry Price - (0.5 × ATR) for PUT

    :param data: DataFrame containing 'close', 'high', 'low'
    :return: Tuple (stop_loss, take_profit)
    """
    data["ATR"] = calculate_atr(data, period=14)
    latest = data.iloc[-1]

    atr_half = 0.5 * latest["ATR"]

    if check_trade_signal(data) == "CALL":
        stop_loss = latest["close"] - atr_half
        take_profit = latest["close"] + atr_half
    elif check_trade_signal(data) == "PUT":
        stop_loss = latest["close"] + atr_half
        take_profit = latest["close"] - atr_half
    else:
        stop_loss, take_profit = None, None

    return stop_loss, take_profit
