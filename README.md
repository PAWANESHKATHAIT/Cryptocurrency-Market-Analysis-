Cryptocurrency Market Analytics Project

1. Introduction
This project automates the extraction, transformation, loading, and analysis of real-time cryptocurrency market data. It establishes a robust data pipeline that fetches data from a public API, stores it in a structured local MySQL database, enriches it with analytical segments, and visualizes key insights through an interactive Power BI dashboard. This README focuses on the Local Development Phase of the project.

2. Architecture Overview
The project follows a classic ETL (Extract, Transform, Load) pattern, orchestrated by Python scripts.

graph LR
    A[CoinGecko API] --> B{Python ETL Scripts};
    B -- Fetch & Transform --> C[Local MySQL Database];
    C -- Store Raw Data --> D[crypto_prices Table];
    D -- Read & Segment --> B2{Python Segmentation Script};
    B2 -- Update --> D;
    D -- Connect --> E[Power BI Desktop];
    E -- Visualize --> F[Interactive Dashboard];

(Note: A detailed draw.io architecture diagram can be provided separately.)

3. Features
Automated Data Extraction: Fetches real-time cryptocurrency market data from the CoinGecko API.

Data Transformation: Cleans and structures raw API data into a database-friendly format.

Incremental Loading: Efficiently inserts new records or updates existing ones in the database based on unique identifiers (timestamp, coin_id).

Market Cap Segmentation: Automatically categorizes cryptocurrencies into tiers (e.g., Large Cap, Mid Cap, Small Cap, Micro/Nano Cap) for enhanced analysis.

Orchestrated Pipeline: Ensures sequential and consistent execution of data loading and segmentation processes.

Interactive Dashboard: Provides a Power BI dashboard for visualizing key market trends, performance metrics, and segmented insights.

4. Prerequisites
Before you begin, ensure you have the following installed:

Python 3.8+: Download Python

MySQL Server: [suspicious link removed]

MySQL Workbench: Download MySQL Workbench (Recommended for database management)

Power BI Desktop: Download Power BI Desktop

MySQL Connector/NET: (Required for Power BI to connect to MySQL) Download Connector/NET - Ensure you install the version compatible with your Power BI Desktop installation (usually the latest GA version).

5. Setup and Installation
Follow these steps to set up the project on your local machine.

5.1. MySQL Database Setup
Start MySQL Server: Ensure your MySQL server is running.

Create Database: Open MySQL Workbench, connect to your MySQL server, and execute the following SQL query to create the database:

CREATE DATABASE IF NOT EXISTS crypto_db;
USE crypto_db;

Create crypto_prices Table: Execute the following SQL query to create the crypto_prices table. This table includes a composite primary key (timestamp, coin_id) to handle unique entries and enable updates.

CREATE TABLE IF NOT EXISTS crypto_prices (
    timestamp DATETIME NOT NULL,
    coin_id VARCHAR(255) NOT NULL,
    symbol VARCHAR(50),
    name VARCHAR(255),
    current_price DECIMAL(20, 8),
    market_cap BIGINT,
    total_volume BIGINT,
    high_24h DECIMAL(20, 8),
    low_24h DECIMAL(20, 8),
    price_change_24h DECIMAL(20, 8),
    price_change_percentage_24h DECIMAL(20, 8),
    market_cap_change_24h BIGINT,
    market_cap_change_percentage_24h DECIMAL(20, 8),
    circulating_supply DECIMAL(30, 8),
    total_supply DECIMAL(30, 8),
    max_supply DECIMAL(30, 8),
    ath DECIMAL(20, 8),
    atl DECIMAL(20, 8),
    PRIMARY KEY (timestamp, coin_id)
);

Add market_cap_tier Column: Add the segmentation column to your crypto_prices table.

ALTER TABLE crypto_prices
ADD COLUMN market_cap_tier VARCHAR(255);

(Optional: To verify, run DESCRIBE crypto_prices;)

5.2. Python Environment Setup
Clone the Repository (or create project folder):
Create a project directory, e.g., CryptoMarketAnalytics.

Create a Virtual Environment:
Navigate to your project directory in the terminal and run:

python -m venv venv

Activate the Virtual Environment:

Windows: .\venv\Scripts\activate

macOS/Linux: source venv/bin/activate

Install Dependencies:
Install the necessary Python libraries:

pip install requests mysql-connector-python pandas sqlalchemy tabulate

Place Python Scripts:
Ensure the following Python files are in your project directory:

etl_crypto.py

segment_and_load.py

pipeline_orchestrator.py

(Make sure the content of these files matches the latest versions provided in our conversation, especially with the refactored functions and the MYSQL_CONFIG details.)

Important MYSQL_CONFIG:
Verify that the MYSQL_CONFIG dictionary in etl_crypto.py and segment_and_load.py matches your MySQL setup:

MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Kathait@1122', # Your MySQL root password
    'database': 'crypto_db'
}

5.3. Running the Data Pipeline
Ensure MySQL is Running: Confirm your MySQL server is active.

Activate Virtual Environment: If not already active, activate your Python virtual environment.

Execute the Orchestrator: Run the main pipeline orchestrator script:

python pipeline_orchestrator.py

This script will:

Fetch the latest cryptocurrency data from CoinGecko.

Load/update this data into your crypto_prices table.

Calculate and update the market_cap_tier for all records in the crypto_prices table.

(Run this script multiple times over a period (e.g., hourly or daily) to accumulate historical data for trend analysis in Power BI.)

6. Power BI Dashboard Setup
Install MySQL Connector/NET: Ensure you have the correct version of MySQL Connector/NET installed for Power BI to connect to your MySQL database.

Open Power BI Desktop.

Get Data:

Go to Home tab -> Get Data -> More...

Search for "MySQL database" and click Connect.

Enter Server: localhost, Database: crypto_db.

Select Data Connectivity mode: DirectQuery (or Import if preferred for smaller datasets/faster initial load). Click OK.

Enter your MySQL Username: root and Password: Kathait@1122 under the "Database" tab. Click Connect.

Load Table:

In the Navigator window, expand crypto_db and select the crypto_prices table.

Click Load.

Data Cleaning (Power Query Editor):

Go to Home tab -> Transform data to open Power Query Editor.

Select crypto_db crypto_prices table.

For numerical columns (current_price, market_cap, total_volume, high_24h, low_24h, etc.), check for and replace empty values with 0 (or another suitable imputation strategy) using Transform -> Replace Values.

Ensure data types are correct (e.g., Decimal Number for prices, Whole Number for volumes/market caps).

Click Home -> Close & Apply.

Create DAX Measures:

Daily Price Range Measure:

Right-click on crypto_db crypto_prices table in "Fields" pane -> New measure.

Formula: Daily Price Range = AVERAGEX('crypto_db crypto_prices', 'crypto_db crypto_prices'[high_24h] - 'crypto_db crypto_prices'[low_24h])

Market Cap Tier Order Column (for logical sorting):

Go to Data view -> Select crypto_db crypto_prices table -> New column.

Formula:

Market Cap Tier Order =
SWITCH(
    'crypto_db crypto_prices'[market_cap_tier],
    "Large Cap (> $100B)", 1,
    "Mid Cap ($1B - $100B)", 2,
    "Small Cap ($100M - $1B)", 3,
    "Micro/Nano Cap (< $100M)", 4,
    BLANK()
)

Select the market_cap_tier column in Data view -> Column tools -> Sort by column -> choose Market Cap Tier Order.

Build Visualizations:

Create the dashboard with the title "Cryptocurrency Market Analytics Dashboard".

Implement the following visuals as discussed, mapping fields to axes/values and applying formatting:

Overall Market KPIs (Card visuals)

Average 24h Price Change by Market Cap Tier (Bar/Column Chart)

Total Market Capitalization Distribution by Tier (Donut Chart)

Top 5 Gainers/Losers (Table visuals with conditional formatting)

Top 10 Cryptocurrencies by 24h Trading Volume (Bar Chart)

Average 24h Price Range by Market Cap Tier (Bar Chart)

(Optional: Individual Coin Price Trend - requires historical data accumulation)

7. Usage
To update the data in your Power BI dashboard:

Ensure your MySQL server is running.

Run the Python orchestrator script: python pipeline_orchestrator.py

In Power BI Desktop, click the Refresh button (in the Home tab) to pull the latest data from your MySQL database.

8. Future Enhancements (Cloud Deployment)
This project is designed with future scalability in mind. The next phase involves deploying the pipeline to AWS for automation and robustness:

AWS RDS: Migrate the local MySQL database to a managed AWS RDS MySQL instance.

AWS Lambda: Deploy the Python pipeline scripts as serverless functions.

AWS EventBridge: Schedule Lambda functions to run automatically at regular intervals.

AWS Secrets Manager: Securely manage database credentials.

Power BI Cloud Connection: Update the Power BI dashboard to connect to the AWS RDS instance.

9. Key Skills Demonstrated
Data Engineering: ETL pipeline development, data orchestration, incremental loading.

Python Programming: API integration, data manipulation with Pandas, database interaction (mysql-connector-python, SQLAlchemy).

Database Management: MySQL schema design, DDL/DML operations, basic administration.

Data Modeling & Transformation: Creating derived metrics and analytical segments (e.g., market_cap_tier).

Business Intelligence: Power BI dashboard design, visualization best practices, DAX formula creation, data connectivity.

Cloud Concepts (Future): Understanding of serverless computing (Lambda), managed databases (RDS), and cloud security.

Troubleshooting & Problem Solving: Identifying and resolving technical issues across the stack.

10. License
This project is open-sourced under the MIT License. See the LICENSE file for more details.
