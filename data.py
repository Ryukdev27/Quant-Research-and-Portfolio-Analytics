import yfinance as yf
from config import STOCKS

def get_data(start, end):
    data = yf.download(STOCKS, start=start, end=end, auto_adjust=True)["Close"]
    returns = data.pct_change().dropna()
    return data, returns

def get_benchmark(start, end):
    df = yf.download("^NSEI", start=start, end=end, auto_adjust=True, progress=False)
    
    if df.empty:
        raise ValueError("Benchmark data not found")

    returns = df["Close"].pct_change().dropna()
    return returns