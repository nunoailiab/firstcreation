import pandas as pd
import yfinance as yf


def check_stock_above_ema(ticker: str):
    data = yf.download(ticker, period="15d", interval="1d")
    if data.empty:
        raise ValueError(f"No data returned for ticker {ticker}")
    data['EMA10'] = data['Adj Close'].ewm(span=10, adjust=False).mean()
    last_five = data.tail(5)
    mask = (last_five['Open'] > last_five['EMA10']) & (last_five['Close'] > last_five['EMA10'])
    above_ema = last_five[mask]
    return last_five, above_ema

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Analyze open and close prices for the last 5 days and check if they are above the 10-day EMA"
    )
    parser.add_argument("ticker", help="US stock ticker symbol, e.g. AAPL")
    args = parser.parse_args()

    last_five, above_ema = check_stock_above_ema(args.ticker)

    print("Last 5 days with EMA10:")
    print(last_five[['Open', 'Close', 'EMA10']])

    print("\nDays where both open and close were above the 10-day EMA:")
    if above_ema.empty:
        print("None")
    else:
        print(above_ema[['Open', 'Close', 'EMA10']])


if __name__ == "__main__":
    main()
