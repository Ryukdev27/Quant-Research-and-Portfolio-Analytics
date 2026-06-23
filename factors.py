def momentum(price, window=20):
    return price.pct_change(window)

def volatility(returns, window=20):
    return returns.rolling(window).std()