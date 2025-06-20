# Wanderer Scanner Blueprint

This repository contains a basic Python script for scanning the entire U.S. equity universe for stocks meeting Wanderer's technical criteria:

- 6-period Triple Exponential Moving Average (TEMA) crossing above the 20-period Exponential Moving Average (EMA).
- Both the 20-period and 50-period Simple Moving Averages (SMA) must be rising.

The script retrieves the current list of U.S. tickers from NASDAQ Trader, downloads recent price data from Yahoo Finance via `yfinance`, computes indicators using `pandas`, and prints tickers that match the rules.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the scanner:
   ```bash
   python scanner.py
   ```

The script prints the tickers meeting the criteria. Schedule it with cron or another scheduler to run daily.
