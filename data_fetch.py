import requests
import logging
from config import Config  # Make sure config.py has your ACCESS_TOKEN

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def main():
    # Example from Upstox docs
    url = 'https://api.upstox.com/v2/option/contract?instrument_key=NSE_INDEX%7CNifty%2050&expiry_date=2025-03-06'
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {Config.ACCESS_TOKEN}',  # Use your actual access token
    }

    try:
        response = requests.get(url, headers=headers)
        logging.info("HTTP Status Code: %s", response.status_code)
        logging.info("Raw Response: %s", response.text)
        
        response.raise_for_status()  # Raise error for 4xx/5xx
        data = response.json()
        
        # Print or log the result
        logging.info("Option Contracts: %s", data)
    except requests.exceptions.RequestException as e:
        logging.error("Error fetching option contracts: %s", e)

if __name__ == "__main__":
    main()
