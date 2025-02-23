import pandas as pd

def calculate_ema(data: pd.DataFrame, period: int, column: str = "close") -> pd.Series:
    """
    Calculate the Exponential Moving Average (EMA).
    :param data: DataFrame containing price data
    :param period: The period for EMA calculation (e.g., 9, 21)
    :param column: Column name for price data (default: 'close')
    :return: Pandas Series with EMA values
    """
    return data[column].ewm(span=period, adjust=False).mean()

def calculate_vwap(data: pd.DataFrame) -> pd.Series:
    """
    Calculate Volume Weighted Average Price (VWAP).
    :param data: DataFrame containing price data (must include 'close', 'volume', 'high', 'low')
    :return: Pandas Series with VWAP values
    """
    typical_price = (data["high"] + data["low"] + data["close"]) / 3
    return (typical_price * data["volume"]).cumsum() / data["volume"].cumsum()

def calculate_atr(data: pd.DataFrame, period: int = 14) -> pd.Series:
    """
    Calculate the Average True Range (ATR).
    :param data: DataFrame containing 'high', 'low', and 'close' prices
    :param period: The period for ATR calculation (default: 14)
    :return: Pandas Series with ATR values
    """
    high_low = data["high"] - data["low"]
    high_close = (data["high"] - data["close"].shift()).abs()
    low_close = (data["low"] - data["close"].shift()).abs()
    
    true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    atr = true_range.rolling(window=period).mean()
    
    return atr
