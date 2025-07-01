# 🚀 Live Cryptocurrency Data Fetching & Analysis

## 📌 Project Overview
This project fetches live cryptocurrency data for the **top 50 cryptocurrencies** using a public API and performs basic analysis. The data is updated every 5 minutes and is stored in an Excel file with live updates.

## 📂 Project Files
- **`script.py`** → Python script to fetch, analyze, and store cryptocurrency data.
- **`CryptoData.xlsx`** → Excel sheet with live-updating cryptocurrency data.
- **`Crypto_Analysis.pdf` / `.docx`** → Analysis report with insights and graphs.

## 🔍 Features & Analysis
### ✅ Live Data Fetching
- Retrieves data from a public API (e.g., CoinGecko, CoinMarketCap, Binance API).
- Captures details such as:
  - Cryptocurrency Name
  - Symbol
  - Current Price (in USD)
  - Market Capitalization
  - 24-hour Trading Volume
  - 24-hour Price Change (%)

### 📊 Data Analysis
- **Top 5 cryptocurrencies by market capitalization**.
- **Average price of the top 50 cryptocurrencies**.
- **Highest & lowest 24-hour percentage price change**.

### 📈 Visualizations (Graphs in Analysis Report)
- **Top 10 Cryptos by Market Cap** (Pie Chart)
- **Top 5 Highest & Lowest 24h Price Change** (Bar Chart)
- **Market Cap vs. 24h Trading Volume** (Scatter Plot)

## 🛠️ Setup & Execution
### 🔹 Prerequisites
Ensure you have Python installed and required libraries:
```bash
pip install requests pandas openpyxl matplotlib
```

### 🔹 Run the Script
Execute the Python script to fetch and analyze live data:
```bash
python script.py
```

### 🔹 Live Updating in Excel
The **Excel file (`CryptoData.xlsx`)** will be automatically updated every 5 minutes with the latest data.


---
📌 **Author:** Pawanesh Kumar  
📅 **Date:** March 2025  

