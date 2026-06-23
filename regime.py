def market_regime(returns):
    vol = returns.rolling(20).std().mean(axis=1)

    regime = []

    for v in vol:
        if v > vol.mean():
            regime.append("high_vol / bear-like")
        else:
            regime.append("low_vol / bull-like")

    return regime