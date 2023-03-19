from pandas import DataFrame
from typing import Callable

def compute_breakout_signals(df: DataFrame, n_up=15, n_down=11, n_shift=0):
    data= df[['High', 'Low', 'Close']].copy()

    data['Band_up']= data.High.rolling(n_up, min_periods= min(n_up,n_down)).mean().shift(1)
    data['Band_down']= data.Low.rolling(n_down, min_periods= min(n_up, n_down)).mean().shift(1)
    
    data['Bout_up']= (data.Close> data.High.rolling(n_up, min_periods= min(n_up, n_down) ).mean().shift(1))* 1
    data['Bout_down']= (data.Close<  data.Low.rolling(n_down, min_periods= min(n_up, n_down)).mean().shift(1))* 1
   
    data['LONG']= (data.Bout_up== 1) & (data.Bout_up.shift(1)== 0)
    # data['EXIT_LONG']= (data.Bout_down== 1) & (data.Bout_down.shift(1)== 0)
    data['EXIT_LONG']= (data.Bout_up.shift(1)== 1) & (data.Close< data.Band_down)
    
    data['SHORT']= (data.Bout_down== 1) & (data.Bout_down.shift(1)== 0)
    # data['EXIT_SHORT']=(data.Bout_up== 1) & (data.Bout_up.shift(1)== 0)
    data['EXIT_SHORT']= (data.Bout_down.shift(1)== 1) &(data.Close> data.Band_up)
    
    data.LONG= data.LONG.shift(n_shift)
    data.EXIT_LONG= data.EXIT_LONG.shift(n_shift)
    data.SHORT= data.SHORT.shift(n_shift)
    data.EXIT_SHORT= data.EXIT_SHORT.shift(n_shift)
    return data

def get_breakout_strategy(n_up=15, n_down=11, n_shift=0)-> Callable[[DataFrame], DataFrame]:
    """
    Currying strategy to split strategy parameter configuration and strategy execution
    """
    def _compute_breakout_signals(df: DataFrame):
        return compute_breakout_signals(df, n_up, n_down, n_shift)
    return _compute_breakout_signals