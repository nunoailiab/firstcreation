# Stock ADX Screener

This project provides a simple Streamlit application that screens US stocks using the Average Directional Index (ADX). The app fetches the list of S&P 500 tickers from Wikipedia and retrieves historical data via `yfinance`. The ADX calculation is implemented directly in the app so no extra technical-analysis packages are required.

Users can customize the ADX period and threshold to filter stocks. Additional tickers can be provided manually.

## Setup

Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Running

Launch the Streamlit application:

```bash
streamlit run app.py
```
