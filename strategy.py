import pandas as pd

class Strategy:
    def __init__(self, atr_multiplier=0.5, daily_loss_limit=400):
        self.atr_multiplier = atr_multiplier
        self.daily_loss_limit = daily_loss_limit
        self.daily_loss = 0  # Track total daily losses
        self.active_trade = None  # Store current active trade

    def check_trade_conditions(self, df: pd.DataFrame) -> bool:
        """
        Check entry conditions for a trade.
        - Bullish signal for option: At least 2 of (VWAP, EMA Crossover, High RVOL, ADX > 20) + IV Rank > 50
        """
        latest = df.iloc[-1]

        price_above_vwap = latest["close"] > latest["VWAP"]
        ema_crossover = latest["EMA_9"] > latest["EMA_21"]
        high_rvol = latest.get("RVOL", 1) >= 2  # Ensure RVOL is available
        strong_trend = latest.get("ADX", 0) > 20  # Ensure ADX is available
        iv_rank_ok = latest.get("IV_Rank", 0) > 50  # IV Rank is mandatory

        # Count how many of the 4 conditions are met
        conditions_met = sum([price_above_vwap, ema_crossover, high_rvol, strong_trend])

        # Require at least 2 out of 4 conditions + IV Rank mandatory
        return conditions_met >= 2 and iv_rank_ok

    def execute_trade(self, entry_price: float, atr: float):
        """
        Execute a new trade if conditions are met.
        - Initializes trade details (entry price, stop-loss, take-profit).
        - Ensures daily loss limit is not exceeded.
        """
        if self.daily_loss >= self.daily_loss_limit:
            print("Daily loss limit reached. No more trades today.")
            return None

        initial_sl = entry_price - (self.atr_multiplier * atr)
        initial_tp = entry_price + (self.atr_multiplier * atr)

        self.active_trade = {
            "entry_price": entry_price,
            "stop_loss": initial_sl,
            "take_profit": initial_tp,
        }
        return self.active_trade

    def trail_sl_tp(self, trade_details: dict, latest_price: float, atr: float) -> dict:
        """
        Adjusts the stop-loss (SL) and take-profit (TP) dynamically as price moves in favor.
        - CALL: SL & TP move UP when option price increases.
        - PUT: SL & TP move UP when option price increases (since we're bullish on the option's price).
        """
        entry_price = trade_details["entry_price"]
        stop_loss = trade_details["stop_loss"]
        take_profit = trade_details["take_profit"]

        # ATR-based adjustment value
        atr_adjustment = self.atr_multiplier * atr

        if latest_price > entry_price + atr_adjustment:
            stop_loss = max(stop_loss, latest_price - atr_adjustment)
            take_profit = latest_price + atr_adjustment

        return {"entry_price": entry_price, "stop_loss": stop_loss, "take_profit": take_profit}

    def manage_trade(self, latest_price: float, atr: float) -> str:
        """
        Manage active trade:
        - Adjust SL/TP dynamically
        - Exit trade if SL or TP is hit
        - Track daily loss
        """
        if not self.active_trade:
            return "No Active Trade"

        # Update SL/TP dynamically
        self.active_trade = self.trail_sl_tp(self.active_trade, latest_price, atr)

        if latest_price >= self.active_trade["take_profit"]:
            print("Take Profit Hit ✅")
            self.active_trade = None
            return "Take Profit Hit"

        elif latest_price <= self.active_trade["stop_loss"]:
            loss = self.active_trade["entry_price"] - latest_price
            self.daily_loss += abs(loss)  # Track cumulative loss
            print(f"Stop Loss Hit ❌ - Loss: {loss}, Total Daily Loss: {self.daily_loss}")

            self.active_trade = None  # Reset active trade
            return "Stop Loss Hit"

        return "Trade Active"
