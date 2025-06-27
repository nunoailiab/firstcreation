# firstcreation

This repository provides a simple stock scanner that implements the **Wanderer Financial Indicator** (WFI).

`wfi_scanner.py` downloads daily data with `yfinance` and reports tickers where:

- The 6‑period TEMA has crossed above the 20‑day EMA.
- The 20‑day and 50‑day SMAs are both trending upward and sit below the current price.

## Requirements

```bash
pip install yfinance pandas
```

## Usage

```
python wfi_scanner.py AAPL MSFT GOOGL
```

The script prints the tickers that satisfy the WFI conditions.
