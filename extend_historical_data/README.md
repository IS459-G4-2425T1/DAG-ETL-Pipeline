# Project Overview

This repository contains files for two EC2 scraper instances:
- **historical data scraper** (for a one-time scrape of past data)
- **scheduled scraper** (for ongoing, scheduled scraping).

## File Descriptions

- **`historical_main.py`**:  
  The primary script for the historical data scraper EC2 instance. It performs a one-off data scrape from 2008 to 2024 to fill gaps between Kaggle data and recent records. This script has hardcoded values for the years and months to scrape.

- **`scheduler_main.py`**:  
  The main script for the scheduled scraper EC2 instance. Unlike `historical_main.py`, this script dynamically derives the current date and scrapes the most recent data available on the BTS site, typically 3 months prior to today.

- **`process_data.py`**:  
  A core processing script used by both scrapers. It merges all scraped CSV files for arrivals and departures into a single CSV and uploads it to the specified S3 bucket.

- **`requirements.txt`**:  
  Lists all dependencies needed to run the scraper. Run this file during initial setup to install the required packages.

- **`run_and_shutdown_bash`**:  
  A bash script located in the scheduled scraper EC2 instance's `rc.local` file. This script automatically initiates the scraper (`scheduler_main.py`) and then shuts down the instance once execution is complete.
