def get_benchmark(start, end):
    import yfinance as yf

    df = yf.download("^NSEI", start=start, end=end, auto_adjust=True, progress=False)

    if df.empty:
        raise ValueError("Benchmark data not found")

    close = df["Close"]

    returns = close.pct_change().dropna()

    return returns