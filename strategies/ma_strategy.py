def strategy_MA(df, **kwargs):
    n = kwargs.get("n", 50)
    ma_type = kwargs.get("ma_type", "sma")
    ma_type = ma_type.strip().lower()
    n_shift = kwargs.get("n_shift", 0)

    data = df.copy()

    if ma_type == "sma":
        sma = ta.trend.SMAIndicator(data.Close, n)
        data["MA"] = sma.sma_indicator().round(4)
    elif ma_type == "ema":
        ema = ta.trend.EMAIndicator(data.Close, n)
        data["MA"] = ema.ema_indicator().round(4)

    data["CLOSE_PREV"] = data.Close.shift(1)

    data["LONG"] = (data.Close > data.MA) & (data.CLOSE_PREV <= data.MA)
    data["EXIT_LONG"] = (data.Close < data.MA) & (data.CLOSE_PREV >= data.MA)

    data["SHORT"] = (data.Close < data.MA) & (data.CLOSE_PREV >= data.MA)
    data["EXIT_SHORT"] = (data.Close > data.MA) & (data.CLOSE_PREV <= data.MA)

    data.LONG = data.LONG.shift(n_shift)
    data.EXIT_LONG = data.EXIT_LONG.shift(n_shift)
    data.SHORT = data.SHORT.shift(n_shift)
    data.EXIT_SHORT = data.EXIT_SHORT.shift(n_shift)

    return data
