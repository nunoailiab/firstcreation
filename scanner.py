import pandas as pd
import yfinance as yf
import requests
from datetime import datetime, timedelta


def get_all_us_tickers():
    """Fetch the list of all US tickers from NASDAQ Trader."""
    urls = [
        "https://ftp.nasdaqtrader.com/dynamic/SymDir/nasdaqlisted.txt",
        "https://ftp.nasdaqtrader.com/dynamic/SymDir/otherlisted.txt",
    ]
    tickers = []
    for url in urls:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except Exception as exc:
            print(f"Failed to fetch {url}: {exc}")
            continue
        lines = response.text.splitlines()[1:]
        for line in lines:
            parts = line.split("|")
            symbol = parts[0]
            if symbol in {"File Creation Time"}:
                break
            if any(c in symbol for c in {"$", "^", "."}):
                continue
            tickers.append(symbol)
    return tickers


def ema(series, span):
    return series.ewm(span=span, adjust=False).mean()


def tema(series, span):
    ema1 = ema(series, span)
    ema2 = ema1.ewm(span=span, adjust=False).mean()
    ema3 = ema2.ewm(span=span, adjust=False).mean()
    return 3 * (ema1 - ema2) + ema3


def compute_indicators(df):
    df = df.copy()
    df["EMA20"] = ema(df["Close"], span=20)
    df["TEMA6"] = tema(df["Close"], span=6)
    df["SMA20"] = df["Close"].rolling(window=20).mean()
    df["SMA50"] = df["Close"].rolling(window=50).mean()
    return df


def is_rising(series):
    if len(series) < 2:
        return False
    return series.iloc[-1] > series.iloc[-2]


def check_crossover(df):
    df = compute_indicators(df)
    if len(df) < 50:
        return False
    last = df.iloc[-1]
    prev = df.iloc[-2]
    crossover = last["TEMA6"] > last["EMA20"] and prev["TEMA6"] <= prev["EMA20"]
    rising_sma = is_rising(df["SMA20"]) and is_rising(df["SMA50"])
    return crossover and rising_sma


def scan(tickers):
    results = []
    end = datetime.now()
    start = end - timedelta(days=120)
    for ticker in tickers:
        try:
            df = yf.download(ticker, start=start, end=end, progress=False)
            if df.empty:
                continue
            if check_crossover(df):
                results.append(ticker)
        except Exception as exc:
            print(f"Error processing {ticker}: {exc}")
    return results


def main():
    tickers = get_all_us_tickers()
    print(f"Scanning {len(tickers)} tickers...")
    matches = scan(tickers)
    print("Tickers meeting criteria:")
    for ticker in matches:
        print(ticker)


if __name__ == "__main__":
    main()
