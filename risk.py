import numpy as np

def sharpe(r):
    return np.sqrt(252) * r.mean() / r.std()


def max_drawdown(equity):
    peak = equity.cummax()
    dd = (equity - peak) / peak
    return dd.min()


def var(r):
    return np.percentile(r, 5)


def cvar(r):
    v = var(r)
    return r[r <= v].mean()


def beta(strategy, market):
    return np.cov(strategy, market)[0][1] / np.var(market)


def hit_ratio(r):
    return (r > 0).mean()