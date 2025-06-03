# Stock Analysis Script

This repository includes a simple Python script, `stock_analysis.py`, which downloads
US stock data for the last few days using `yfinance` and checks whether each of the
last five daily open and close prices are above the 10-day exponential moving
average (EMA).

## Setup

1. Install dependencies (requires Python 3):

   ```bash
   pip install pandas yfinance
   ```

## Usage

Run the script from the command line and pass the ticker symbol of the stock you
want to analyze:

```bash
python stock_analysis.py AAPL
```

Replace `AAPL` with the ticker of the US stock you are interested in.
