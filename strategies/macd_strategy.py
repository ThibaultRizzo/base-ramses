def strategy_MACD(df, **kwargs):
    
    n_slow= kwargs.get('n_slow', 26)
    n_fast= kwargs.get('n_fast', 12)
    n_sign= kwargs.get('n_sign', 9)
    n_shift= kwargs.get('n_shift', 0)
    
    data= df.copy()
    
    macd= ta.trend.MACD(data.Close, n_slow, n_fast, n_sign)
    
    data['MACD_DIFF']= macd.macd_diff().round(4)
    data['MACD_DIFF_PREV']= data.MACD_DIFF.shift(1)
    
    data['LONG']= (data.MACD_DIFF> 0) & (data.MACD_DIFF_PREV<=0)
    data['EXIT_LONG']= (data.MACD_DIFF< 0) & (data.MACD_DIFF_PREV>= 0)
    
    data['SHORT']= (data.MACD_DIFF< 0) & (data.MACD_DIFF_PREV>=0)
    data['EXIT_SHORT']= (data.MACD_DIFF> 0) & (data.MACD_DIFF_PREV<= 0)
    
    data.LONG= data.LONG.shift(n_shift)
    data.EXIT_LONG= data.EXIT_LONG.shift(n_shift)
    data.SHORT= data.SHORT.shift(n_shift)
    data.EXIT_SHORT= data.EXIT_SHORT.shift(n_shift)
   
    return data

