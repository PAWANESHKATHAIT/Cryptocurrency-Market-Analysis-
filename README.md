Cryptocurrency Market Analytics Project
This project establishes a robust data pipeline for extracting, transforming, loading, and analyzing real-time cryptocurrency market data, culminating in an interactive Power BI dashboard. This README provides an overview of the project's goals, architecture, and key components developed during the Local Development Phase.

Project Goal
The primary objective is to deliver up-to-date insights into the cryptocurrency market. This is achieved by systematically collecting data from a public API, storing it in a structured local database, enriching it with analytical segments, and presenting these insights through a dynamic visualization dashboard.

Architecture and Components (Local Development Phase)
The project is built around a classic ETL (Extract, Transform, Load) pipeline, orchestrated by Python scripts and leveraging a local MySQL database for data storage and Power BI for visualization.

1. Data Source
CoinGecko API: Serves as the external source for raw, real-time cryptocurrency market data, including current prices, market capitalization, trading volumes, and 24-hour changes.

2. ETL Pipeline (Python Scripts)
The data pipeline is managed by a set of interconnected Python scripts:

etl_crypto.py (Extract & Initial Load):

Functionality: Connects to the CoinGecko API, fetches market data for a specified number of cryptocurrencies, transforms the raw JSON response into a structured format, and loads it into the local MySQL database.

Key Feature: Utilizes ON DUPLICATE KEY UPDATE logic in MySQL to efficiently handle existing records (based on timestamp and coin_id), ensuring data freshness without creating duplicate entries.

segment_and_load.py (Data Segmentation & Update):

Functionality: Reads the crypto_prices data from the MySQL database and performs a crucial analytical transformation. It calculates a market_cap_tier (e.g., 'Large Cap', 'Mid Cap', 'Small Cap', 'Micro/Nano Cap') for each cryptocurrency based on its market capitalization.

Key Feature: Updates the existing crypto_prices table by populating the market_cap_tier column, ensuring all relevant data, including analytical segments, resides in a single, unified table.

pipeline_orchestrator.py (Pipeline Orchestration):

Functionality: Acts as the master control script for the entire data pipeline. It ensures sequential execution by first calling etl_crypto.py to load the latest data, and then, immediately afterward, calls segment_and_load.py to apply the segmentation.

Purpose: Guarantees data consistency and reliability by ensuring that segmentation is performed only after the most recent data has been successfully loaded, preventing incomplete or outdated analysis.

3. Local Database
MySQL (crypto_db): A dedicated MySQL database hosts the crypto_prices table.

crypto_prices Table: This table is the central repository for all extracted, transformed, and segmented cryptocurrency data. It was initially set up manually and is continuously updated by the Python pipeline. The market_cap_tier column has been successfully integrated into this table.

Role: Provides a structured and accessible storage layer for all analytical data.

4. Visualization
Power BI Dashboard: An interactive dashboard built using Power BI Desktop, directly connected to the local MySQL crypto_db and the crypto_prices table.

Dashboard Title: "Cryptocurrency Market Analytics Dashboard"

Key Visualizations:

Overall Market KPIs: Card visuals displaying high-level metrics (Total Market Capitalization, Total 24h Trading Volume, Average 24h Price Change %).

Market Cap Tier Performance: Bar charts illustrating Average 24h Price Change and Average 24h Price Range by market_cap_tier segments.

Market Dominance: A Donut Chart showing the distribution of Total Market Capitalization across market_cap_tier segments.

Top/Bottom Performers: Table visuals with conditional formatting identifying the Top 5 Gainers, Top 5 Losers by 24h price change, and the Top 10 Cryptocurrencies by 24h Trading Volume.

Current Status: The dashboard is fully functional and provides insightful analysis based on current snapshot data. Historical trend analysis visuals will become fully effective as more data is accumulated over time through repeated pipeline runs.

Key Learnings and Skills Demonstrated
This project showcases practical experience and proficiency in:

API Integration: Interacting with external web APIs for data extraction.

Python for Data Engineering: Developing scripts for ETL processes, including data cleaning, transformation, and database interaction.

Database Management (MySQL): Database setup, table creation, data manipulation (inserting, updating), and schema modification.

Data Transformation & Enhancement: Implementing business logic to create new, analytically valuable features (e.g., market cap segmentation).

Data Orchestration: Designing and implementing a sequential workflow for interdependent data processes.

Business Intelligence (Power BI): Connecting to data sources, building diverse interactive visualizations, creating custom DAX measures, and applying conditional formatting for enhanced insights.

Troubleshooting: Systematically identifying and resolving technical issues encountered during pipeline development.

Next Steps (Future Work)
The project is designed for future scalability and automation. The next phase involves Cloud Deployment to AWS, specifically:

Migrating the MySQL database to AWS RDS.

Deploying the Python pipeline scripts to AWS Lambda.

Automating the pipeline execution using AWS EventBridge.

Implementing secure credential management via AWS Secrets Manager.

Updating the Power BI dashboard to connect to the cloud-hosted AWS RDS database.

This project, even in its current local form, represents a robust and highly relevant data analytics solution, demonstrating a comprehensive skill set valuable in real-world data engineering and business intelligence roles.
