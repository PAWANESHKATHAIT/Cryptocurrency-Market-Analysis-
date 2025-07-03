import pandas as pd
import mysql.connector
from mysql.connector import Error
from sqlalchemy import create_engine
import urllib.parse

# --- MySQL Database Connection Details ---
# IMPORTANT: These should match the details you used in etl_crypto.py
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Kathait@1122', # Your provided password
    'database': 'crypto_db' # Ensure this matches your database name
}

# --- Function to get a MySQL connection ---
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

# --- Main script for segmentation and updating existing table ---
def run_segmentation_update():
    """
    Executes the market cap segmentation and updates the existing 'crypto_prices' table.
    """
    print("Starting market cap segmentation and updating existing 'crypto_prices' table in MySQL...")

    try:
        encoded_password = urllib.parse.quote_plus(MYSQL_CONFIG['password'])
        db_connection_str = (
            f"mysql+mysqlconnector://{MYSQL_CONFIG['user']}:"
            f"{encoded_password}@{MYSQL_CONFIG['host']}/"
            f"{MYSQL_CONFIG['database']}"
        )
        db_connection = create_engine(db_connection_str)

        print("Fetching data from 'crypto_prices' table for segmentation...")
        df_crypto = pd.read_sql("SELECT timestamp, coin_id, market_cap FROM crypto_prices", db_connection)
        print(f"Successfully fetched {len(df_crypto)} records for segmentation.")

        # --- Perform Market Cap Segmentation ---
        bins = [0, 100_000_000, 1_000_000_000, 100_000_000_000, float('inf')]
        labels = ['Micro/Nano Cap (< $100M)', 'Small Cap ($100M - $1B)', 'Mid Cap ($1B - $100B)', 'Large Cap (> $100B)']

        df_crypto['market_cap_tier'] = pd.cut(
            df_crypto['market_cap'],
            bins=bins,
            labels=labels,
            right=True,
            include_lowest=True
        )

        print("\n--- Sample Data with Market Cap Segmentation (First 10 records) ---")
        print(df_crypto[['coin_id', 'market_cap', 'market_cap_tier']].head(10).to_markdown(index=False))
        print("-------------------------------------------------------------------")

        print("\nUpdating 'market_cap_tier' in the 'crypto_prices' table...")
        conn = get_mysql_connection()
        if conn:
            cursor = conn.cursor()
            update_sql = """
            UPDATE crypto_prices
            SET market_cap_tier = %s
            WHERE timestamp = %s AND coin_id = %s;
            """
            updated_count = 0
            for index, row in df_crypto.iterrows():
                try:
                    # Convert pandas.Categorical to string before passing to MySQL connector
                    cursor.execute(update_sql, (str(row['market_cap_tier']), row['timestamp'], row['coin_id']))
                    updated_count += cursor.rowcount
                except Error as e:
                    print(f"Error updating row for {row['coin_id']} at {row['timestamp']}: {e}")
            
            conn.commit()
            print(f"Successfully updated {updated_count} records in 'crypto_prices' table.")
        else:
            print("Could not establish connection to update the table.")

    except Error as e:
        print(f"An error occurred during Python segmentation and updating: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    print("Market cap segmentation and update process finished.")

# This block allows segment_and_load.py to be run directly for testing,
# but its primary use will be via the orchestration script.
if __name__ == "__main__":
    run_segmentation_update()
