import requests
import json
import time
from datetime import datetime
import mysql.connector
from mysql.connector import Error

# --- Configuration ---
COINGECKO_API_URL = "https://api.coingecko.com/api/v3/coins/markets"
VS_CURRENCY = "usd"
TARGET_ROWS = 250
MAX_PER_PAGE = 250

# MySQL Database Connection Details - UPDATED WITH YOUR PROVIDED INFORMATION
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Kathait@1122',
    'database': 'crypto_db'
}

# --- Function to fetch data from CoinGecko API (Extract) ---
def fetch_crypto_data(vs_currency: str, per_page: int, page: int) -> list:
    """
    Fetches live cryptocurrency market data from CoinGecko API.
    """
    params = {
        "vs_currency": vs_currency,
        "per_page": per_page,
        "page": page,
        "sparkline": "false",
        "price_change_percentage": "1h,24h,7d"
    }
    print(f"Fetching data from: {COINGECKO_API_URL} with params: {params}")

    try:
        response = requests.get(COINGECKO_API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        print(f"Successfully fetched {len(data)} cryptocurrencies for page {page}.")
        return data
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err} - Response: {response.text}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An unexpected error occurred: {req_err}")
    except json.JSONDecodeError as json_err:
        print(f"JSON decode error: {json_err} - Response text: {response.text}")
    return []

# --- Function to transform data (Transform) ---
def transform_data(raw_data: list) -> list:
    """
    Transforms the raw cryptocurrency data into a more structured format.
    """
    transformed_records = []
    timestamp = datetime.now().isoformat()

    for coin in raw_data:
        record = {
            "timestamp": timestamp,
            "coin_id": coin.get("id"),
            "symbol": coin.get("symbol"),
            "name": coin.get("name"),
            "current_price": coin.get("current_price"),
            "market_cap": coin.get("market_cap"),
            "total_volume": coin.get("total_volume"),
            "high_24h": coin.get("high_24h"),
            "low_24h": coin.get("low_24h"),
            "price_change_24h": coin.get("price_change_24h"),
            "price_change_percentage_24h": coin.get("price_change_percentage_24h"),
            "market_cap_change_24h": coin.get("market_cap_change_24h"),
            "market_cap_change_percentage_24h": coin.get("market_cap_change_percentage_24h"),
            "circulating_supply": coin.get("circulating_supply"),
            "total_supply": coin.get("total_supply"),
            "max_supply": coin.get("max_supply"),
            "ath": coin.get("ath"),
            "atl": coin.get("atl")
        }
        transformed_records.append(record)
    return transformed_records

# --- Database functions (Load) ---
def get_mysql_connection():
    """Establishes and returns a connection to the MySQL database."""
    try:
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        if conn.is_connected():
            print(f"Successfully connected to MySQL database: {MYSQL_CONFIG['database']}")
        return conn
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None

def insert_data_mysql(data: list):
    """
    Inserts transformed cryptocurrency data into the crypto_prices table in MySQL.
    Uses ON DUPLICATE KEY UPDATE to handle existing records based on unique key (timestamp, coin_id).
    """
    conn = get_mysql_connection()
    if conn:
        cursor = conn.cursor()
        insert_sql = """
        INSERT INTO crypto_prices (
            timestamp, coin_id, symbol, name, current_price, market_cap,
            total_volume, high_24h, low_24h, price_change_24h,
            price_change_percentage_24h, market_cap_change_24h,
            market_cap_change_percentage_24h, circulating_supply, total_supply,
            max_supply, ath, atl
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            current_price = VALUES(current_price),
            market_cap = VALUES(market_cap),
            total_volume = VALUES(total_volume),
            high_24h = VALUES(high_24h),
            low_24h = VALUES(low_24h),
            price_change_24h = VALUES(price_change_24h),
            price_change_percentage_24h = VALUES(price_change_percentage_24h),
            market_cap_change_24h = VALUES(market_cap_change_24h),
            market_cap_change_percentage_24h = VALUES(market_cap_change_percentage_24h),
            circulating_supply = VALUES(circulating_supply),
            total_supply = VALUES(total_supply),
            max_supply = VALUES(max_supply),
            ath = VALUES(ath),
            atl = VALUES(atl);
        """
        rows_to_insert = []
        for record in data:
            rows_to_insert.append((
                record.get("timestamp"), record.get("coin_id"), record.get("symbol"),
                record.get("name"), record.get("current_price"), record.get("market_cap"),
                record.get("total_volume"), record.get("high_24h"), record.get("low_24h"),
                record.get("price_change_24h"), record.get("price_change_percentage_24h"),
                record.get("market_cap_change_24h"), record.get("market_cap_change_percentage_24h"),
                record.get("circulating_supply"), record.get("total_supply"),
                record.get("max_supply"), record.get("ath"), record.get("atl")
            ))

        try:
            cursor.executemany(insert_sql, rows_to_insert)
            conn.commit()
            print(f"Successfully inserted/updated {cursor.rowcount} records into MySQL.")
        except Error as e:
            print(f"MySQL database error during data insertion: {e}")
            conn.rollback()
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

# --- Main ETL process function ---
def run_etl_load():
    """
    Executes the full ETL (Extract, Transform, Load) process.
    """
    print("Starting ETL process (Extract, Transform, Load)...")
    all_raw_crypto_data = []
    current_page = 1
    fetched_count = 0

    while fetched_count < TARGET_ROWS:
        items_to_fetch_this_page = min(MAX_PER_PAGE, TARGET_ROWS - fetched_count)
        if items_to_fetch_this_page <= 0:
            break

        raw_data_page = fetch_crypto_data(VS_CURRENCY, items_to_fetch_this_page, current_page)
        if raw_data_page:
            all_raw_crypto_data.extend(raw_data_page)
            fetched_count += len(raw_data_page)
            current_page += 1
            time.sleep(0.5)
        else:
            print(f"Failed to fetch data from page {current_page}. Stopping.")
            break

    if all_raw_crypto_data:
        transformed_crypto_data = transform_data(all_raw_crypto_data)
        print(f"Total transformed {len(transformed_crypto_data)} records.")
        insert_data_mysql(transformed_crypto_data)
    else:
        print("No data fetched. Please check API connection or parameters.")
    print("ETL process finished.")

# This block allows etl_crypto.py to be run directly for testing,
# but its primary use will be via the orchestration script.
if __name__ == "__main__":
    run_etl_load()
