import pandas as pd

from data import get_data, get_benchmark
from factors import momentum, volatility
from signals import generate_signal, rank_signal
from strategies import equal_weight, top_decile, long_short
from backtest import backtest
from risk import sharpe, max_drawdown, var, cvar, hit_ratio


def run_pipeline(start, end, strategy):

    # =========================
    # DATA
    # =========================
    price, returns = get_data(start, end)
    bench_returns = get_benchmark(start, end)

    # Guard against get_benchmark() returning a single-column DataFrame
    # instead of a Series (e.g. df[["NIFTY50"]] vs df["NIFTY50"]).
    # squeeze("columns") collapses (n, 1) -> (n,) and leaves a Series untouched.
    if isinstance(bench_returns, pd.DataFrame):
        bench_returns = bench_returns.squeeze("columns")

    # keep structure (DO NOT FLATTEN EVERYTHING)
    returns = returns.dropna()
    bench_returns = bench_returns.dropna()

    # align index properly
    common_index = returns.index.intersection(bench_returns.index)

    if len(common_index) < 10:
        raise ValueError("Not enough overlapping data")

    returns = returns.loc[common_index]
    bench_returns = bench_returns.loc[common_index]
    price = price.loc[common_index]

    # =========================
    # FACTORS (correct)
    # =========================
    mom = momentum(price)
    vol = volatility(returns)

    signal = generate_signal(mom, vol)
    rank = rank_signal(signal)

    # =========================
    # STRATEGY
    # =========================
    if strategy == "Equal Weight":
        weights = equal_weight(rank)
    elif strategy == "Top Decile":
        weights = top_decile(signal)
    else:
        weights = long_short(signal)

    # =========================
    # BACKTEST
    # =========================
    strat_returns, equity = backtest(weights, returns)

    # Guard against backtest() returning single-column DataFrames instead
    # of Series (same class of bug as bench_returns above).
    if isinstance(strat_returns, pd.DataFrame):
        strat_returns = strat_returns.squeeze("columns")
    if isinstance(equity, pd.DataFrame):
        equity = equity.squeeze("columns")

    strat_returns = strat_returns.dropna()
    equity = equity.loc[strat_returns.index]

    # =========================
    # BENCHMARK EQUITY
    # =========================
    bench_equity = (1 + bench_returns).cumprod()
    bench_equity = bench_equity.loc[bench_equity.index.intersection(strat_returns.index)]
    bench_equity = bench_equity.reindex(strat_returns.index)

    # =========================
    # ALPHA
    # =========================
    aligned_bench = bench_returns.reindex(strat_returns.index)
    alpha_series = strat_returns - aligned_bench
    alpha_cum = (1 + alpha_series).cumprod()

    # =========================
    # METRICS (REALISTIC NOW)
    # =========================
    metrics = {
        "sharpe": float(sharpe(strat_returns)),
        "max_drawdown": float(max_drawdown(equity)),
        "var": float(var(strat_returns)),
        "cvar": float(cvar(strat_returns)),
        "hit_ratio": float(hit_ratio(strat_returns)),

        "final_value": float(equity.iloc[-1]),
        "benchmark_final": float(bench_equity.iloc[-1]),
        "alpha_final": float(alpha_cum.iloc[-1])
    }

    return strat_returns, equity, bench_equity, alpha_cum, metrics