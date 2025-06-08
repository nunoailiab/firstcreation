import argparse
import pandas as pd
import yfinance as yf


def get_filtered_tickers(tickers, min_price, max_price, period="1mo"):
    filtered = []
    data = yf.download(tickers, period=period, auto_adjust=False, progress=False)
    if isinstance(tickers, str):
        tickers = [tickers]
    for ticker in tickers:
        try:
            df = data['Adj Close'][ticker].dropna()
        except Exception:
            df = yf.download(ticker, period=period, progress=False)['Adj Close'].dropna()
        if df.empty or len(df) < 20:
            continue
        ema10 = df.ewm(span=10).mean().iloc[-1]
        ema20 = df.ewm(span=20).mean().iloc[-1]
        last_price = df.iloc[-1]
        if last_price > ema10 and last_price > ema20 and min_price <= last_price <= max_price:
            filtered.append((ticker, last_price))
    return filtered


def main():
    parser = argparse.ArgumentParser(description="Filter tickers by EMA and price range")
    parser.add_argument("tickers", nargs='+', help="List of tickers to check")
    parser.add_argument("--min", dest="min_price", type=float, required=True, help="Minimum closing price")
    parser.add_argument("--max", dest="max_price", type=float, required=True, help="Maximum closing price")
    parser.add_argument("--period", default="1mo", help="Data period for EMA calculation (e.g., 6mo, 1y)")
    args = parser.parse_args()

    result = get_filtered_tickers(args.tickers, args.min_price, args.max_price, args.period)
    if result:
        print("Tickers above 10 EMA, above 20 EMA, within price range:")
        for ticker, price in result:
            print(f"{ticker}: {price:.2f}")
    else:
        print("No tickers match the criteria.")


if __name__ == "__main__":
    main()
