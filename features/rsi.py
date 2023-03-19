from ta import momentum
from pandas import DataFrame
from typing import Callable

def compute_rsi(df: DataFrame, rsi_window=14):
    rsi= momentum.RSIIndicator(df['Close'], rsi_window)
    return DataFrame({"RSI": rsi.rsi().round(4)})
