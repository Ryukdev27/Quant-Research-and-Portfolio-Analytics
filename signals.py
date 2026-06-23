def generate_signal(momentum, volatility):
    signal = 0.7 * momentum - 0.3 * volatility
    return signal


def rank_signal(signal):
    return signal.rank(axis=1, ascending=False)