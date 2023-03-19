from ta import momentum
from pandas import DataFrame
from typing import Callable

def compute_rsi_signals(data: DataFrame, n: int, n_seuil: int, n_shift: int):
    data = data.copy()
    rsi= momentum.RSIIndicator(data.Close, n)
    data['RSI']= rsi.rsi().round(4)
    data['RSI_PREV']= data.RSI.shift(1)
    
    data['LONG']= (data.RSI> n_seuil) & (data.RSI_PREV <= n_seuil)
    data['EXIT_LONG']= (data.RSI< 100- n_seuil) & (data.RSI_PREV>= 100- n_seuil)
    
    data['SHORT']= (data.RSI< 100- n_seuil) & (data.RSI_PREV >= 100- n_seuil)
    data['EXIT_SHORT']= (data.RSI> n_seuil) & (data.RSI_PREV <= n_seuil)
    
    data.LONG= data.LONG.shift(n_shift)
    data.EXIT_LONG= data.EXIT_LONG.shift(n_shift)
    data.SHORT= data.SHORT.shift(n_shift)
    data.EXIT_SHORT= data.EXIT_SHORT.shift(n_shift)
    
    return data

def get_rsi_strategy(n=14, n_seuil=30, n_shift=0)-> Callable[[DataFrame], DataFrame]:
    """
    Currying strategy to split strategy parameter configuration and strategy execution
    """
    def _compute_rsi_signals(df: DataFrame):
        return compute_rsi_signals(df, n, n_seuil, n_shift)
    return _compute_rsi_signals