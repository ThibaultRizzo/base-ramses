import numpy as np
import pandas as pd
import ta
import yfinance as yf


##################################################################
def strategy_Breakout(df, **kwargs):
    n_up = kwargs.get("n_up", 15)
    n_down = kwargs.get("n_down", 11)
    n_shift = kwargs.get("n_shift", 0)

    data = df[["High", "Low", "Close"]].copy()

    data["Band_up"] = data.High.rolling(n_up, min_periods=min(n_up, n_down)).mean().shift(1)
    data["Band_down"] = data.Low.rolling(n_down, min_periods=min(n_up, n_down)).mean().shift(1)

    data["Bout_up"] = (data.Close > data.High.rolling(n_up, min_periods=min(n_up, n_down)).mean().shift(1)) * 1
    data["Bout_down"] = (data.Close < data.Low.rolling(n_down, min_periods=min(n_up, n_down)).mean().shift(1)) * 1

    data["LONG"] = (data.Bout_up == 1) & (data.Bout_up.shift(1) == 0)
    # data['EXIT_LONG']= (data.Bout_down== 1) & (data.Bout_down.shift(1)== 0)
    data["EXIT_LONG"] = (data.Bout_up.shift(1) == 1) & (data.Close < data.Band_down)

    data["SHORT"] = (data.Bout_down == 1) & (data.Bout_down.shift(1) == 0)
    # data['EXIT_SHORT']=(data.Bout_up== 1) & (data.Bout_up.shift(1)== 0)
    data["EXIT_SHORT"] = (data.Bout_down.shift(1) == 1) & (data.Close > data.Band_up)

    data.LONG = data.LONG.shift(n_shift)
    data.EXIT_LONG = data.EXIT_LONG.shift(n_shift)
    data.SHORT = data.SHORT.shift(n_shift)
    data.EXIT_SHORT = data.EXIT_SHORT.shift(n_shift)

    return data


############################################################################################################
def strategy_RSI(df, **kwargs):
    n = kwargs.get("n", 14)
    n_seuil = 30
    n_shift = kwargs.get("n_shift", 0)

    data = df.copy()
    rsi = ta.momentum.RSIIndicator(data.Close, n)
    data["RSI"] = rsi.rsi().round(4)
    data["RSI_PREV"] = data.RSI.shift(1)

    data["LONG"] = (data.RSI > n_seuil) & (data.RSI_PREV <= n_seuil)
    data["EXIT_LONG"] = (data.RSI < 100 - n_seuil) & (data.RSI_PREV >= 100 - n_seuil)

    data["SHORT"] = (data.RSI < 100 - n_seuil) & (data.RSI_PREV >= 100 - n_seuil)
    data["EXIT_SHORT"] = (data.RSI > n_seuil) & (data.RSI_PREV <= n_seuil)

    data.LONG = data.LONG.shift(n_shift)
    data.EXIT_LONG = data.EXIT_LONG.shift(n_shift)
    data.SHORT = data.SHORT.shift(n_shift)
    data.EXIT_SHORT = data.EXIT_SHORT.shift(n_shift)

    return data


###############################################################
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


###############################################################
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


###############################################################
def strategy_MACD(df, **kwargs):
    n_slow = kwargs.get("n_slow", 26)
    n_fast = kwargs.get("n_fast", 12)
    n_sign = kwargs.get("n_sign", 9)
    n_shift = kwargs.get("n_shift", 0)

    data = df.copy()

    macd = ta.trend.MACD(data.Close, n_slow, n_fast, n_sign)

    data["MACD_DIFF"] = macd.macd_diff().round(4)
    data["MACD_DIFF_PREV"] = data.MACD_DIFF.shift(1)

    data["LONG"] = (data.MACD_DIFF > 0) & (data.MACD_DIFF_PREV <= 0)
    data["EXIT_LONG"] = (data.MACD_DIFF < 0) & (data.MACD_DIFF_PREV >= 0)

    data["SHORT"] = (data.MACD_DIFF < 0) & (data.MACD_DIFF_PREV >= 0)
    data["EXIT_SHORT"] = (data.MACD_DIFF > 0) & (data.MACD_DIFF_PREV <= 0)

    data.LONG = data.LONG.shift(n_shift)
    data.EXIT_LONG = data.EXIT_LONG.shift(n_shift)
    data.SHORT = data.SHORT.shift(n_shift)
    data.EXIT_SHORT = data.EXIT_SHORT.shift(n_shift)

    return data


###############################################################
def strategy_Ichimoku(df, **kwargs):
    n_conv = kwargs.get("n_conv", 9)
    n_base = kwargs.get("n_base", 26)
    n_span_b = kwargs.get("n_span_b", 26)

    data = df.copy()

    ichimoku = ta.trend.IchimokuIndicator(data.High, data.Low, n_conv, n_base, n_span_b)

    data["BASE"] = ichimoku.ichimoku_base_line().round(4)
    data["CONV"] = ichimoku.ichimoku_conversion_line().round(4)

    data["DIFF"] = data["CONV"] - data["BASE"]
    data["DIFF_PREV"] = data["DIFF"].shift(1)

    data["LONG"] = (data.DIFF > 0) & (data.DIFF_PREV <= 0)
    data["EXIT_LONG"] = (data.DIFF < 0) & (data.DIFF_PREV >= 0)

    data["SHORT"] = (data.DIFF < 0) & (data.DIFF_PREV >= 0)
    data["EXIT_SHORT"] = (data.DIFF > 0) & (data.DIFF_PREV <= 0)

    data.LONG = data.LONG.shift(1)
    data.EXIT_LONG = data.EXIT_LONG.shift(1)
    data.SHORT = data.SHORT.shift(1)
    data.EXIT_SHORT = data.EXIT_SHORT.shift(1)

    return data


################################################################
def strategy_WR(df, **kwargs):
    n = kwargs.get("n", 14)

    data = df.copy()

    wr = ta.momentum.WilliamsRIndicator(data.High, data.Low, data.Close, n)

    data["WR"] = wr.WR().round(4)
    data["WR_PREV"] = data.WR.shift(1)

    data["LONG"] = (data.WR > -80) & (data.WR_PREV <= -80)
    data["EXIT_LONG"] = (data.WR < -20) & (data.WR_PREV >= -20)

    data["SHORT"] = (data.WR < -20) & (data.WR_PREV >= -20)
    data["EXIT_SHORT"] = (data.WR > -80) & (data.WR_PREV <= -80)

    data.LONG = data.LONG.shift(1)
    data.EXIT_LONG = data.EXIT_LONG.shift(1)
    data.SHORT = data.SHORT.shift(1)
    data.EXIT_SHORT = data.EXIT_SHORT.shift(1)

    return data


###############################################################
def strategy_KeltnerChannel_origin(df, **kwargs):
    n = kwargs.get("n", 10)
    data = df.copy()

    k_band = ta.volatility.KeltnerChannel(data.High, data.Low, data.Close, n)

    data["K_BAND_UB"] = k_band.keltner_channel_hband().round(4)
    data["K_BAND_LB"] = k_band.keltner_channel_lband().round(4)

    data["CLOSE_PREV"] = data.Close.shift(1)

    data["LONG"] = (data.Close <= data.K_BAND_LB) & (data.CLOSE_PREV > data.K_BAND_LB)
    data["EXIT_LONG"] = (data.Close >= data.K_BAND_UB) & (data.CLOSE_PREV < data.K_BAND_UB)

    data["SHORT"] = (data.Close >= data.K_BAND_UB) & (data.CLOSE_PREV < data.K_BAND_UB)
    data["EXIT_SHORT"] = (data.Close <= data.K_BAND_LB) & (data.CLOSE_PREV > data.K_BAND_LB)

    data.LONG = data.LONG.shift(1)
    data.EXIT_LONG = data.EXIT_LONG.shift(1)
    data.SHORT = data.SHORT.shift(1)
    data.EXIT_SHORT = data.EXIT_SHORT.shift(1)

    return data


#############################################################
