-- Create Database
CREATE DATABASE IF NOT EXISTS crypto_db;

USE crypto_db;

-- Create the crypto_prices table if it doesn't exist
CREATE TABLE IF NOT EXISTS crypto_prices (
    id INT AUTO_INCREMENT PRIMARY KEY,   -- Auto-incrementing ID for each record
    timestamp VARCHAR(255) NOT NULL,     -- Timestamp when the data was fetched (ISO format)
    coin_id VARCHAR(255) NOT NULL,       -- Unique ID of the cryptocurrency (e.g., 'bitcoin')
    symbol VARCHAR(255) NOT NULL,        -- Symbol of the cryptocurrency (e.g., 'btc')
    name VARCHAR(255) NOT NULL,          -- Name of the cryptocurrency (e.g., 'Bitcoin')
    current_price DOUBLE,                -- Current price in USD
    market_cap DOUBLE,                   -- Market capitalization
    total_volume DOUBLE,                 -- 24h total trading volume
    high_24h DOUBLE,                     -- 24h high price
    low_24h DOUBLE,                      -- 24h low price
    price_change_24h DOUBLE,             -- 24h price change
    price_change_percentage_24h DOUBLE,  -- 24h price change percentage
    market_cap_change_24h DOUBLE,        -- 24h market cap change
    market_cap_change_percentage_24h DOUBLE, -- 24h market cap change percentage
    circulating_supply DOUBLE,           -- Circulating supply
    total_supply DOUBLE,                 -- Total supply
    max_supply DOUBLE,                   -- Max supply
    ath DOUBLE,                          -- All Time High price
    atl DOUBLE,                          -- All Time Low price
    UNIQUE KEY (timestamp, coin_id)      -- Ensure unique records for a given coin at a specific timestamp
);

SELECT * FROM crypto_prices LIMIT 5;

SELECT COUNT(*) FROM crypto_prices;

ALTER TABLE crypto_prices
ADD COLUMN market_cap_tier VARCHAR(255);

SELECT market_cap_tier FROM crypto_prices LIMIT 5;


