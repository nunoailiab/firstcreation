# firstcreation

This repository contains an example script for filtering stock tickers that
are above their 10-day and 20-day exponential moving averages (EMAs) and fall
within a user-specified price range. The script, `ema_filter.py`, uses the
`yfinance` and `pandas` libraries to download historical price data and perform
the calculations.

## Requirements

- Python 3
- `yfinance` and `pandas` (install via `pip install yfinance pandas`)

## Usage

```bash
python ema_filter.py TICKER1 TICKER2 --min MIN_PRICE --max MAX_PRICE [--period 6mo]
```

Example:

```bash
python ema_filter.py AAPL MSFT --min 100 --max 200 --period 6mo
```

This will print any tickers that currently close above both the 10 EMA and
20 EMA with a closing price between the specified minimum and maximum.
Note: The script requires internet access to download data from Yahoo Finance.
