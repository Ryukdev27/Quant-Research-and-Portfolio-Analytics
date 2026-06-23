from config import TOP_N

# Equal Weight Strategy
def equal_weight(rank):
    weights = rank.copy()
    weights[:] = 0

    for date in rank.index:
        top = rank.loc[date].nsmallest(TOP_N).index
        weights.loc[date, top] = 1 / TOP_N

    return weights


# Top Decile Strategy
def top_decile(signal):
    weights = signal.copy()
    weights[:] = 0

    for date in signal.index:
        threshold = signal.loc[date].quantile(0.9)
        selected = signal.loc[date][signal.loc[date] >= threshold].index
        if len(selected) > 0:
            weights.loc[date, selected] = 1 / len(selected)

    return weights


# Long Short Strategy
def long_short(signal):
    weights = signal.copy()
    weights[:] = 0

    for date in signal.index:
        sorted_s = signal.loc[date].sort_values()

        longs = sorted_s.tail(TOP_N).index
        shorts = sorted_s.head(TOP_N).index

        weights.loc[date, longs] = 1 / TOP_N
        weights.loc[date, shorts] = -1 / TOP_N

    return weights