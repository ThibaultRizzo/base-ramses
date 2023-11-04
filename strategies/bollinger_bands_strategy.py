def strategy_BollingerBands(df, **kwargs):
    n = kwargs.get("n", 10)
    n_rng = kwargs.get("n_rng", 2)
    n_shift = kwargs.get("n_shift", 0)

    data = df.copy()
    boll = ta.volatility.BollingerBands(data.Close, n, n_rng)

    data["BOLL_LBAND_INDI"] = boll.bollinger_lband_indicator()
    data["BOLL_HBAND_INDI"] = boll.bollinger_hband_indicator()
    data["CLOSE_PREV"] = data.Close.shift(1)

    data["LONG"] = data.BOLL_LBAND_INDI == 1
    data["EXIT_LONG"] = data.BOLL_HBAND_INDI == 1

    data["SHORT"] = data.BOLL_HBAND_INDI == 1
    data["EXIT_SHORT"] = data.BOLL_LBAND_INDI == 1

    data.LONG = data.LONG.shift(n_shift)
    data.EXIT_LONG = data.EXIT_LONG.shift(n_shift)
    data.SHORT = data.SHORT.shift(n_shift)
    data.EXIT_SHORT = data.EXIT_SHORT.shift(n_shift)

    return data
