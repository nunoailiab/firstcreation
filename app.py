import streamlit as st
import pandas as pd
import yfinance as yf
import numpy as np

def calculate_adx(high: pd.Series, low: pd.Series, close: pd.Series, window: int = 14) -> pd.Series:
    """Return the Average Directional Index for the given data."""
    high = high.reset_index(drop=True)
    low = low.reset_index(drop=True)
    close = close.reset_index(drop=True)

    up_move = high.diff()
    down_move = low.shift(1) - low
    plus_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0.0)
    minus_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0.0)

    tr = pd.concat([
        high - low,
        (high - close.shift()).abs(),
        (low - close.shift()).abs(),
    ], axis=1).max(axis=1)

    atr = tr.ewm(alpha=1/window, adjust=False).mean()
    plus_di = 100 * pd.Series(plus_dm).ewm(alpha=1/window, adjust=False).mean() / atr
    minus_di = 100 * pd.Series(minus_dm).ewm(alpha=1/window, adjust=False).mean() / atr

    dx = 100 * (plus_di - minus_di).abs() / (plus_di + minus_di)
    adx = dx.ewm(alpha=1/window, adjust=False).mean()
    return adx

@st.cache_data
def get_sp500_tickers():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    tables = pd.read_html(url)
    return tables[0]['Symbol'].tolist()

@st.cache_data(show_spinner=False)
def fetch_history(ticker, period="6mo", interval="1d"):
    return yf.download(ticker, period=period, interval=interval)

st.title("ADX Stock Screener")

st.write(
    "This app screens S&P 500 stocks based on the Average Directional Index (ADX)."
)

period = st.number_input("ADX period", min_value=1, value=14)
threshold = st.number_input("ADX threshold", min_value=1, value=25)

additional = st.text_input(
    "Additional tickers (comma separated)", value="")
extra_tickers = [t.strip().upper() for t in additional.split(',') if t.strip()]

run = st.button("Run Screener")

if run:
    tickers = get_sp500_tickers() + extra_tickers
    results = []
    progress = st.progress(0.0)
    for i, ticker in enumerate(tickers):
        df = fetch_history(ticker)
        if not df.empty:
            adx = calculate_adx(df['High'], df['Low'], df['Close'], window=period)
            if not adx.empty and adx.iloc[-1] >= threshold:
                results.append({"Ticker": ticker, "ADX": round(adx.iloc[-1], 2)})
        progress.progress((i + 1)/len(tickers))
    progress.empty()
    if results:
        st.dataframe(pd.DataFrame(results).sort_values('ADX', ascending=False))
    else:
        st.write("No stocks matched the criteria.")
