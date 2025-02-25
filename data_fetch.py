import requests
from config import Config  # Import Config class
from urllib.parse import quote
import logging

# Logging Setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Upstox API Credentials
ACCESS_TOKEN = Config.ACCESS_TOKEN
EXCHANGE = Config.EXCHANGE
BASE_URL = Config.BASE_URL

# API Headers
HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

def fetch_option_contract(symbol, expiry_date, option_type, strike_price):
    """
    Fetch option contract details from Upstox API.

    :param symbol: The option's underlying asset (e.g., NIFTY, SENSEX)
    :param expiry_date: The expiry date in YYYYMMDD format
    :param option_type: "CE" for Call, "PE" for Put
    :param strike_price: The strike price of the option
    :return: JSON response with option contract details or None on failure
    """
    # Validate parameters
    if option_type not in ["CE", "PE"]:
        logging.error("Invalid option type. Must be 'CE' (Call) or 'PE' (Put).")
        return None

    if not isinstance(strike_price, (int, float)):
        logging.error("Invalid strike price. Must be a number.")
        return None

    # Construct Instrument Key (Format: EXCHANGE|SYMBOL|EXPIRY_DATE|OPTION_TYPE|STRIKE_PRICE)
    instrument_key = f"{EXCHANGE}|{symbol}|{expiry_date}|{option_type}|{strike_price}"
    encoded_key = quote(instrument_key)  # URL encode

    # Construct URL
    url = f"{BASE_URL}/option/contract?instrument_key={encoded_key}"
    logging.info(f"Fetching contract data from URL: {url}")

    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()  # Raise error for 4xx and 5xx status codes

        data = response.json()

        # Process the response
        if data and data.get("data"):
            logging.info(f"Fetched {len(data['data'])} contract(s).")

            # Extract and print contract details
            for item in data["data"]:
                logging.info(f"Instrument Key: {item.get('instrument_key')}")
                logging.info(f"Trading Symbol: {item.get('trading_symbol')}")
                logging.info(f"Lot Size: {item.get('lot_size')}")
                logging.info(f"Expiry Date: {item.get('expiry')}")
                logging.info(f"Strike Price: {item.get('strike')}")
                logging.info("-" * 50)

            return data

        else:
            logging.warning("No option contract data found.")
            return None

    except requests.exceptions.HTTPError as e:
        logging.error(f"HTTP Error: {e}")
        if e.response:
            logging.error(f"Response Text: {e.response.text}")  # Log API response
        return None

    except requests.exceptions.RequestException as e:
        logging.error(f"Request Error: {e}")
        return None

# Debugging Example Call
if __name__ == "__main__":
    test_symbol = "NIFTY"
    test_expiry = "20250327"  # Example expiry date (YYYYMMDD)
    test_option_type = "CE"
    test_strike = 22000

    fetch_option_contract(test_symbol, test_expiry, test_option_type, test_strike)
