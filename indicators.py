import pandas as pd
import numpy as np

class Indicators:
    """
    A class to encapsulate all indicator calculations for a trading algorithm.
    This includes EMA, VWAP, ATR, ADX, EMA Slope, RVOL, and IV Rank.
    """

    @staticmethod
    def calculate_ema(data: pd.DataFrame, period: int, column: str = "close") -> pd.Series:
        """
        Calculate the Exponential Moving Average (EMA) for a given price column.
        
        Parameters:
            data (pd.DataFrame): DataFrame containing price data.
            period (int): The period for the EMA calculation (e.g., 9, 21).
            column (str): The column name for the price data (default is "close").
        
        Returns:
            pd.Series: A Series of EMA values.
        """
        return data[column].ewm(span=period, adjust=False).mean()

    @staticmethod
    def calculate_vwap(data: pd.DataFrame, price_type: str = "typical") -> pd.Series:
        """
        Calculate the Volume Weighted Average Price (VWAP) for a DataFrame.
        
        Parameters:
            data (pd.DataFrame): DataFrame containing price data; must include 'high', 'low', 'close', and 'volume' columns.
            price_type (str): Type of price to use:
                - "typical": Uses Typical Price = (High + Low + Close) / 3 (default)
                - "close": Uses the closing price.
        
        Returns:
            pd.Series: A Series with VWAP values.
        """
        if price_type == "typical":
            price = (data["high"] + data["low"] + data["close"]) / 3
        elif price_type == "close":
            price = data["close"]
        else:
            raise ValueError("Invalid price_type. Use 'typical' or 'close'.")
        # Using cumulative sums to compute VWAP
        vwap = (price * data["volume"]).cumsum() / data["volume"].cumsum()
        return vwap

    @staticmethod
    def calculate_atr(data: pd.DataFrame, period: int = 14) -> pd.Series:
        """
        Calculate the Average True Range (ATR) to measure volatility.
        
        Parameters:
            data (pd.DataFrame): DataFrame containing 'high', 'low', and 'close' prices.
            period (int): The period for ATR calculation (default is 14).
        
        Returns:
            pd.Series: A Series with ATR values. Missing values at the start are handled by setting min_periods=1.
        """
        high_low = data["high"] - data["low"]
        high_close = (data["high"] - data["close"].shift()).abs()
        low_close = (data["low"] - data["close"].shift()).abs()
        
        true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        atr = true_range.rolling(window=period, min_periods=1).mean()  # Avoid NaNs by using min_periods=1
        return atr

    @staticmethod
    def calculate_adx(data: pd.DataFrame, period: int = 14) -> pd.Series:
        """
        Calculate the Average Directional Index (ADX) to determine trend strength.
        
        Parameters:
            data (pd.DataFrame): DataFrame containing 'high', 'low', and 'close' prices.
            period (int): The period for ADX calculation (default is 14).
        
        Returns:
            pd.Series: A Series with ADX values. Uses a small constant to avoid division by zero.
        """
        up_move = data["high"].diff()
        down_move = data["low"].diff()

        plus_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0)
        minus_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0)

        tr1 = data["high"] - data["low"]
        tr2 = (data["high"] - data["close"].shift()).abs()
        tr3 = (data["low"] - data["close"].shift()).abs()
        true_range = np.maximum.reduce([tr1, tr2, tr3])
        
        plus_di = 100 * pd.Series(plus_dm).rolling(window=period, min_periods=1).sum() / (
            pd.Series(true_range).rolling(window=period, min_periods=1).sum() + 1e-9)
        minus_di = 100 * pd.Series(minus_dm).rolling(window=period, min_periods=1).sum() / (
            pd.Series(true_range).rolling(window=period, min_periods=1).sum() + 1e-9)
        dx = (abs(plus_di - minus_di) / (plus_di + minus_di + 1e-9)) * 100
        adx = dx.rolling(window=period, min_periods=1).mean()
        return adx

    @staticmethod
    def calculate_ema_slope(data: pd.DataFrame, period: int, column: str = "close") -> pd.Series:
        """
        Calculate the slope of the EMA for trend analysis.
        
        Parameters:
            data (pd.DataFrame): DataFrame containing price data.
            period (int): The period for the EMA to calculate its slope.
            column (str): The column to base the EMA calculation on (default is 'close').
        
        Returns:
            pd.Series: A Series representing the first derivative of the EMA (slope).
        """
        ema = Indicators.calculate_ema(data, period, column)
        ema_slope = ema.diff()  # First derivative (rate of change)
        return ema_slope

    @staticmethod
    def calculate_rvol(data: pd.DataFrame, period: int = 20) -> pd.Series:
        """
        Calculate Relative Volume (RVOL) as current volume divided by the average volume over a given period.
        
        Parameters:
            data (pd.DataFrame): DataFrame containing 'volume' column.
            period (int): The period over which to average the volume (default is 20).
        
        Returns:
            pd.Series: A Series of RVOL values.
        """
        avg_volume = data["volume"].rolling(window=period, min_periods=1).mean()
        rvol = data["volume"] / (avg_volume + 1e-9)  # Avoid division by zero
        return rvol

    @staticmethod
    def calculate_iv_rank(data: pd.DataFrame, iv_col: str = "IV", period: int = 252) -> pd.Series:
        """
        Calculate the Implied Volatility (IV) Rank over a specified period.
        
        IV Rank = (Current IV - Minimum IV) / (Maximum IV - Minimum IV) * 100
        
        Parameters:
            data (pd.DataFrame): DataFrame containing the IV data.
            iv_col (str): Column name for IV data (default is "IV").
            period (int): Number of periods (e.g., trading days) over which to calculate IV Rank (default is 252).
        
        Returns:
            pd.Series: A Series with IV Rank values between 0 and 100.
        """
        iv = data[iv_col]
        min_iv = iv.rolling(window=period, min_periods=1).min()
        max_iv = iv.rolling(window=period, min_periods=1).max()
        iv_rank = ((iv - min_iv) / (max_iv - min_iv + 1e-9)) * 100
        return iv_rank
