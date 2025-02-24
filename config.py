import os

class Config:
    """
    Configuration settings for the trading algorithm.
    All sensitive information is retrieved from environment variables.
    """

    # Upstox API Credentials (must be set in environment variables)
    API_KEY: str = os.getenv("UPSTOX_API_KEY")
    API_SECRET: str = os.getenv("UPSTOX_API_SECRET")
    ACCESS_TOKEN: str = os.getenv("UPSTOX_ACCESS_TOKEN")

    if not API_KEY or not API_SECRET or not ACCESS_TOKEN:
        raise ValueError("API credentials not set in environment variables. "
                         "Please set UPSTOX_API_KEY, UPSTOX_API_SECRET, and UPSTOX_ACCESS_TOKEN.")

    # Trading Settings
    LOT_SIZE_NIFTY: int = int(os.getenv("LOT_SIZE_NIFTY", "75"))
    LOT_SIZE_SENSEX: int = int(os.getenv("LOT_SIZE_SENSEX", "20"))
    MAX_RISK_PER_TRADE: float = float(os.getenv("MAX_RISK_PER_TRADE", "400.0"))
    MAX_DAILY_LOSS: float = float(os.getenv("MAX_DAILY_LOSS", "400.0"))
    TARGET_PROFIT: float = float(os.getenv("TARGET_PROFIT", "1000.0"))

    # Indicator Settings
    EMA_SHORT: int = int(os.getenv("EMA_SHORT", "9"))
    EMA_LONG: int = int(os.getenv("EMA_LONG", "21"))
    ADX_PERIOD: int = int(os.getenv("ADX_PERIOD", "14"))
    ATR_PERIOD: int = int(os.getenv("ATR_PERIOD", "14"))
    VWAP_SOURCE: str = os.getenv("VWAP_SOURCE", "typical")  # 'typical' or 'close'
    RVOL_LOOKBACK: int = int(os.getenv("RVOL_LOOKBACK", "20"))
    IV_RANK_LOOKBACK: int = int(os.getenv("IV_RANK_LOOKBACK", "252"))

    # Order Execution Settings
    SL_TP_TRAIL_FACTOR: float = float(os.getenv("SL_TP_TRAIL_FACTOR", "0.5"))
    MIN_IV_RANK: float = float(os.getenv("MIN_IV_RANK", "30.0"))
    MIN_RVOL: float = float(os.getenv("MIN_RVOL", "2.0"))

    # API Endpoints
    BASE_URL: str = os.getenv("BASE_URL", "https://api.upstox.com/v2")
    
    # Logging Settings
    LOG_FILE: str = os.getenv("LOG_FILE", "trading_log.txt")
    DEBUG_MODE: bool = os.getenv("DEBUG_MODE", "True").lower() in ["true", "1", "yes"]
