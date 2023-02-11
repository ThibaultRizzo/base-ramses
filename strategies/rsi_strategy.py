from ta import momentum
from pandas import DataFrame

def compute_rsi(df: DataFrame, rsi_window=14):
    rsi= momentum.RSIIndicator(df['Close'], rsi_window)
    return DataFrame({"RSI": rsi.rsi().round(4)})

def compute_rsi_signals(data: DataFrame, n_seuil=30, n_shift=0):
    print(f"data   {data}")
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


def strategy_rsi(df, n=14, n_seuil=30, n_shift=0):
    data= df.copy()
    rsi= ta.momentum.RSIIndicator(data.Close, n)
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
