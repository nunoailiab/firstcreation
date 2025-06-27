import argparse
import pandas as pd
import yfinance as yf


def tema(series: pd.Series, length: int) -> pd.Series:
    """Calculate Triple Exponential Moving Average."""
    ema1 = series.ewm(span=length, adjust=False).mean()
    ema2 = ema1.ewm(span=length, adjust=False).mean()
    ema3 = ema2.ewm(span=length, adjust=False).mean()
    return 3 * ema1 - 3 * ema2 + ema3


def compute_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["TEMA6"] = tema(df["Close"], 6)
    df["EMA20"] = df["Close"].ewm(span=20, adjust=False).mean()
    df["SMA20"] = df["Close"].rolling(window=20).mean()
    df["SMA50"] = df["Close"].rolling(window=50).mean()
    return df


def qualifies(df: pd.DataFrame) -> bool:
    if len(df) < 51:
        return False
    last = df.iloc[-1]
    prev = df.iloc[-2]
    cross = prev["TEMA6"] <= prev["EMA20"] and last["TEMA6"] > last["EMA20"]
    slopes = last["SMA20"] > prev["SMA20"] and last["SMA50"] > prev["SMA50"]
    below_price = last["SMA20"] < last["Close"] and last["SMA50"] < last["Close"]
    return cross and slopes and below_price


def scan(tickers):
    results = []
    for ticker in tickers:
        try:
            data = yf.download(ticker, period="3mo", interval="1d", progress=False)
            if data.empty:
                continue
            df = compute_indicators(data)
            if qualifies(df):
                results.append(ticker)
        except Exception as exc:
            print(f"Failed to process {ticker}: {exc}")
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Scan for Wanderer Financial Indicator")
    parser.add_argument("tickers", nargs="+", help="Ticker symbols to scan")
    args = parser.parse_args()
    matches = scan(args.tickers)
    if matches:
        print("WFI candidates:")
        for sym in matches:
            print(sym)
    else:
        print("No symbols matched")


if __name__ == "__main__":
    main()
