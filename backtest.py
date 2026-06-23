import numpy as np
from config import TRANSACTION_COST, SLIPPAGE


def compute_cost(weights):
    turnover = weights.diff().abs().sum(axis=1)
    return turnover * (TRANSACTION_COST + SLIPPAGE)


def backtest(weights, returns):
    weights = weights.shift(1).fillna(0)

    strat_returns = (weights * returns).sum(axis=1)

    cost = compute_cost(weights)

    strat_returns = strat_returns - cost

    equity = (1 + strat_returns).cumprod()

    return strat_returns, equity