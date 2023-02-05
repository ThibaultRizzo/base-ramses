# -*- coding: utf-8 -*-
"""
Created on Sun Jul 31 18:19:30 2022

@author: 33688
"""


import yfinance as yf
import ta
import pandas as pd
import numpy as np
from datetime import date, timedelta, datetime
from itertools import product
import matplotlib.pyplot as plt

############################################################################################################ 
# download data
############################################################################################################ 
def get_stock_data(ticker, start_date, end_date, buffer_days= 365):
    
# ticker= 'ISF.L'
# start_date= '2019-01-01'
# end_date= '2019-12-31'

    date_fmt= '%Y-%m-%d'

    start_date_buffer= datetime.strptime(start_date, date_fmt)- timedelta(days= buffer_days)
    start_date_buffer= start_date_buffer.strftime(date_fmt)

    df= yf.download(ticker, start= start_date_buffer, end= end_date)
    return df
############################################################################################################ 
####   FONCTIONS UTILITAIRES
############################################################################################################      
def target_point(P0, HLC, profit_move, stop_move, eps):
# calcule le target d'un point P0 à l'origine d'une série HLC, avec un objectif de profit_move et
# un stop-loss de stop_move
    S= HLC.copy()
    S.columns= ['High', 'Low', 'Close']
    ret_high= S.High/ P0 - 1
    ret_high= ret_high.reset_index(drop= True)
    ret_low=S.Low/ P0 - 1
    ret_low= ret_low.reset_index(drop= True)
    
    if (ret_high> profit_move).sum()>0:
        N_up_profit= ret_high.loc[ret_high> profit_move].index[0]
    else:
        N_up_profit= 999
        
    if (ret_high> stop_move).sum()>0:
        N_up_sloss= ret_high.loc[ret_high> stop_move].index[0]
    else:
        N_up_sloss= 999   
        
    if (ret_low<- profit_move).sum()>0:
        N_down_profit= ret_low.loc[ret_low<- profit_move].index[0]
    else:
        N_down_profit= 999
    
    if (ret_low<- stop_move).sum()>0:
        N_down_sloss= ret_low.loc[ret_low<- stop_move].index[0]
    else:
        N_down_sloss= 999 
     
    if N_up_profit< N_down_profit:
        target= 1/ (1+  eps)**N_up_profit- (N_down_sloss< N_up_profit)/ (1+  eps)**N_down_sloss
    elif N_down_profit< N_up_profit:
        target= -1/ (1+  eps)**N_down_profit+ (N_up_sloss< N_down_profit)/ (1+  eps)**N_up_sloss
    else:
        target= 0
        
    return target
###############################################################
def target_series(HLC, n_days_limit, profit_move, stop_move, eps= 0.05):
# calcule le target de tous les points d'une série, avec un objectif de profit_move et
# un stop-loss de stop_move, avec une limite de n_days_limit forward
# par défaut, le premier et dernier points ont un target de 0
    S= HLC.copy()
    S.columns= ['High', 'Low', 'Close']
    
    target= S.iloc[:,0]* 0
    
    for i in range(0,S.shape[0]- 1 - n_days_limit):
        target[i]= target_point(S['Close'][i], S.iloc[i+1:i+1+ n_days_limit], profit_move, stop_move, eps)
    for i in range(S.shape[0]- 1 - n_days_limit, S.shape[0]- 1):
        target[i]= target_point(S['Close'][i], S.iloc[i+1:], profit_move, stop_move, eps)
        
    return target
        
############################################################################################################ 
####   FEATURES
############################################################################################################      
def feature_LargeMoves(HLC, C0, n_days, move):
# calcule le ratio de large directional moves up versus down
# C0 représente le point de référence pour la première barre (ex open ou C(-1))
# move peut être exprimé en % ou en nombre d'ATR passé
# le ratio est entre 0 et 1
    S= HLC.copy()
    S.columns= ['High', 'Low', 'Close']
    ATR_array= np.array([])
    i=0
    ATR_array[i]= max(S.High[i]-C0, C0- Low[i], High[i]- Low[i])
    directional_moves[i]= (ATR_array[i]> move)* \
        (max(High[i]- Close[i], Close[i]- Low[i])< (High[i]- Low[i])/8)
    
    return S
######################################################
def Point_Ref_Simple(S,l):
    # calcule les deux séries de points de référence max et min d'une série
    # pour une moyenne mobile simple de longueur l
    df=pd.DataFrame(S)
    temp=pd.DataFrame(index= df.index, data= np.zeros((len(df),4)))
    temp.iloc[:l,0]=df.iloc[:l,0]
    temp.iloc[:l,1]=df.iloc[:l,0]
    temp.iloc[:l,2]=df.iloc[:l,0]
    temp.iloc[:l,3]=df.iloc[:l,0]

    sma=df.rolling(window=l,center=False).mean()
    sg=(df-sma).apply(np.sign)

    i=l
    sg[:i]=sg.iloc[i][0]
    temp.iloc[:i,1]= np.min(df.iloc[:i,0])
    temp.iloc[:i,2]= np.max(df.iloc[:i,0])

    if sg.iloc[i,0]==1:
        temp.iloc[:i,0]= np.min(df.iloc[:i,0])
    else:
        temp.iloc[:i,0]= np.max(df.iloc[:i,0])

    for i in range(l,len(S)):

        if sg.iloc[i,0]>sg.iloc[i-1,0]:
            temp.iloc[i,0]=df.iloc[i,0]
            temp.iloc[i,1]=temp.iloc[i-1,0]
            temp.iloc[i,2]=temp.iloc[i-1,2]
            temp.iloc[i,3]=temp.iloc[i,1]
            
        elif sg.iloc[i,0]<sg.iloc[i-1,0]:
            temp.iloc[i,0]=df.iloc[i,0]
            temp.iloc[i,1]=temp.iloc[i-1,1]
            temp.iloc[i,2]=temp.iloc[i-1,0]
            temp.iloc[i,3]=temp.iloc[i,2]

        elif sg.iloc[i,0]==1:
            temp.iloc[i,0]=np.max([temp.iloc[i-1,0],df.iloc[i,0]])
            temp.iloc[i,1]=temp.iloc[i-1,1]
            temp.iloc[i,2]=temp.iloc[i-1,2]
            temp.iloc[i,3]=temp.iloc[i,1]
          
        else:
            temp.iloc[i,0]=np.min([temp.iloc[i-1,0],df.iloc[i,0]])
            temp.iloc[i,1]=temp.iloc[i-1,1]
            temp.iloc[i,2]=temp.iloc[i-1,2]
            temp.iloc[i,3]=temp.iloc[i,2]
           
    return temp.iloc[:,1:3]
######################################################
######################################################
def max_DDown_abs(S):
# calcule le max drawdown absolu d'une série S sur une longueur l
    S=pd.DataFrame(S)
    DD=(S.cummax()-S)
    return DD.max()[0]
######################################################
def max_DUp_abs(S):
# calcule le max drawup absolu d'une série S sur une longueur l
    S=pd.DataFrame(S)
    DU=(S-S.cummin())
    return DU.max()[0]
######################################################
##################################################################
def rolling_gen(df, w):
    for i in range(df.shape[0] - w + 1):
        yield pd.DataFrame(df.values[i:i+w, :], df.index[i:i+w], df.columns)
####################################################################
def corde_path(S):
# calcule le ratio entre la corde et le chemin total d'un df de prix
    A=np.array(S.copy())
    
    corde= A[-1]/A[0]-1    
    path= np.sum(np.array([np.abs(A[i]/A[i-1]-1) for i in range(1,len(A))]), axis=0)    
    path[path==0]= np.nan
    
    temp=pd.Series(corde/path,name=S.index[-1])   
    return temp
##########################################################
def F_ts_corde_path(S,l1):
# donne le ratio corde/path sur l1 jours d'une série de prix
    temp0= S* np.nan    
    z=rolling_gen(S,l1)    
    temp=pd.concat([corde_path(item) for item in z],axis=1)
    temp0.loc[temp.T.index]= temp.T  
    return temp0.fillna(0)
############################################################################################################ 
####   STRATEGY
############################################################################################################     
def strategy_Breakout(df, **kwargs):
    
    n_up= kwargs.get('n_up', 15)
    n_down= kwargs.get('n_down', 11)
    n_shift= kwargs.get('n_shift', 0)
    
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
############################################################################################################ 
def strategy_RSI(df, **kwargs):
    
    n= kwargs.get('n', 14)
    n_seuil= 30
    n_shift= kwargs.get('n_shift', 0)
    
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
###############################################################
def strategy_BollingerBands(df, **kwargs):
    
    n= kwargs.get('n', 10)
    n_rng= kwargs.get('n_rng', 2)
    n_shift= kwargs.get('n_shift', 0)
    
    data= df.copy()
    boll= ta.volatility.BollingerBands(data.Close, n, n_rng)
    
    data['BOLL_LBAND_INDI']= boll.bollinger_lband_indicator()
    data['BOLL_HBAND_INDI']=boll.bollinger_hband_indicator()
    data['CLOSE_PREV']= data.Close.shift(1)
    
    data['LONG']= (data.BOLL_LBAND_INDI== 1)
    data['EXIT_LONG']= (data.BOLL_HBAND_INDI== 1)
    
    data['SHORT']= (data.BOLL_HBAND_INDI== 1)
    data['EXIT_SHORT']= (data.BOLL_LBAND_INDI== 1)
    
    data.LONG= data.LONG.shift(n_shift)
    data.EXIT_LONG= data.EXIT_LONG.shift(n_shift)
    data.SHORT= data.SHORT.shift(n_shift)
    data.EXIT_SHORT= data.EXIT_SHORT.shift(n_shift)
    
    return data
###############################################################
def strategy_MA(df, **kwargs):
    
    n= kwargs.get('n', 50)
    ma_type= kwargs.get('ma_type','sma')
    ma_type= ma_type.strip().lower()
    n_shift= kwargs.get('n_shift', 0)
    
    data= df.copy()
    
    if ma_type== 'sma':
       sma= ta.trend.SMAIndicator(data.Close,n)
       data['MA']= sma.sma_indicator().round(4)
    elif ma_type== 'ema':
       ema= ta.trend.EMAIndicator(data.Close,n)
       data['MA']= ema.ema_indicator().round(4) 

    data['CLOSE_PREV']= data.Close.shift(1)
    
    data['LONG']= (data.Close> data.MA) & (data.CLOSE_PREV<= data.MA)
    data['EXIT_LONG']= (data.Close< data.MA) & (data.CLOSE_PREV>= data.MA)
    
    data['SHORT']= (data.Close< data.MA) & (data.CLOSE_PREV>= data.MA)
    data['EXIT_SHORT']= (data.Close> data.MA) & (data.CLOSE_PREV<= data.MA)
    
    data.LONG= data.LONG.shift(n_shift)
    data.EXIT_LONG= data.EXIT_LONG.shift(n_shift)
    data.SHORT= data.SHORT.shift(n_shift)
    data.EXIT_SHORT= data.EXIT_SHORT.shift(n_shift)
    
    return data
###############################################################
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
###############################################################
def strategy_Ichimoku(df, **kwargs):
    n_conv= kwargs.get('n_conv', 9)
    n_base= kwargs.get('n_base', 26)
    n_span_b= kwargs.get('n_span_b', 26)
    
    data= df.copy()
    
    ichimoku= ta.trend.IchimokuIndicator(data.High, data.Low, n_conv, n_base, n_span_b)
    
    data['BASE']= ichimoku.ichimoku_base_line().round(4)
    data['CONV']= ichimoku.ichimoku_conversion_line().round(4)
    
    data['DIFF']= data['CONV']- data['BASE']
    data['DIFF_PREV']= data['DIFF'].shift(1)
    
    data['LONG']= (data.DIFF> 0) & (data.DIFF_PREV<= 0)
    data['EXIT_LONG']= (data.DIFF< 0) & (data.DIFF_PREV>= 0)
    
    data['SHORT']= (data.DIFF< 0) & (data.DIFF_PREV>= 0)
    data['EXIT_SHORT']= (data.DIFF> 0) & (data.DIFF_PREV<= 0)
    
    data.LONG= data.LONG.shift(1)
    data.EXIT_LONG= data.EXIT_LONG.shift(1)
    data.SHORT= data.SHORT.shift(1)
    data.EXIT_SHORT= data.EXIT_SHORT.shift(1)
   
    return data
################################################################
def strategy_WR(df, **kwargs):
    n= kwargs.get('n', 14)
    
    data= df.copy()
    
    wr= ta.momentum.WilliamsRIndicator(data.High, data.Low, data.Close, n)
    
    data['WR']= wr.WR().round(4)
    data['WR_PREV']= data.WR.shift(1)
    
    data['LONG']= (data.WR> -80) & (data.WR_PREV<= -80)
    data['EXIT_LONG']= (data.WR< -20) & (data.WR_PREV>= -20)
    
    data['SHORT']= (data.WR< -20) & (data.WR_PREV>= -20)
    data['EXIT_SHORT']= (data.WR> -80) & (data.WR_PREV<= -80)
    
    data.LONG= data.LONG.shift(1)
    data.EXIT_LONG= data.EXIT_LONG.shift(1)
    data.SHORT= data.SHORT.shift(1)
    data.EXIT_SHORT= data.EXIT_SHORT.shift(1)
   
    return data
###############################################################
def strategy_KeltnerChannel_origin(df, **kwargs):
    n= kwargs.get('n', 10)
    data= df.copy()
    
    k_band= ta.volatility.KeltnerChannel(data.High, data.Low, data.Close, n)
    
    data['K_BAND_UB']= k_band.keltner_channel_hband().round(4)
    data['K_BAND_LB']= k_band.keltner_channel_lband().round(4)
    
    data['CLOSE_PREV']= data.Close.shift(1)
    
    data['LONG']= (data.Close<= data.K_BAND_LB) & (data.CLOSE_PREV> data.K_BAND_LB)
    data['EXIT_LONG']= (data.Close>= data.K_BAND_UB) & (data.CLOSE_PREV< data.K_BAND_UB)
    
    data['SHORT']= (data.Close>= data.K_BAND_UB) & (data.CLOSE_PREV< data.K_BAND_UB)
    data['EXIT_SHORT']= (data.Close<= data.K_BAND_LB) & (data.CLOSE_PREV> data.K_BAND_LB)
    
    data.LONG= data.LONG.shift(1)
    data.EXIT_LONG= data.EXIT_LONG.shift(1)
    data.SHORT= data.SHORT.shift(1)
    data.EXIT_SHORT= data.EXIT_SHORT.shift(1)
    
    return data
############################################################################################################ 
####   SIGNALS  &  RUN STRATEGY  FUNCTIONS
############################################################################################################     

def signal_strategy(df, start_date, end_date, strategy, **kwargs):
 # l'output est le signal de la stratégie pour la journée considérée
    df_strategy= strategy(df, **kwargs)
    signal_df= df_strategy[(df_strategy.index >= start_date) & (df_strategy.index<= end_date)]
    return signal_df
###############################################################
def run_strategy(ticker, signal_df, i0, stop_loss= None, stop_profit= None, regime= None):
    # i0 est la première date de run de la strategy
    # il est bon de séparer la stratégie de Stop-Loss de celle du signal, afin de pouvoir tester plusieurs 
    # stratégies de stop-loss
    # l objectif de la fonction est de fournir une position, un prix d entrée un prix de sortie et des stats
    df= signal_df.copy()
    
    ## variables quotidiennes
    pos= 0
    ey_price_L= np.nan
    ey_price_S= np.nan
    ex_price_L= np.nan
    ex_price_S= np.nan
    n_trades= 0
    n_days_trade_L= 0
    n_days_trade_S= 0
    day_ret= 0
    ## variables discontinues
    trade_ret_L= np.nan
    trade_ret_S= np.nan
    exit_type= np.nan
    trade_summary= []
    ## variables cumulées
    model_position= [0]
    entry_price_L= np.nan
    entry_price_S= np.nan
    exit_price_L= np.nan
    exit_price_S= np.nan
    trade_ret_all_L= 0
    trade_ret_all_S= 0
    n_days_L= 0
    n_days_S= 0
    VL_ret= [0]
    
    for i in range(1, df.shape[0]):


############################################
### Stop Profit 
############################################
        if stop_profit:
            
            if (model_position[i-1]== 1) and (df['High'][i]> entry_price_L[i-1]*(1+ stop_profit)):
                print('stop_profit_L', i)
                pos= 0                
                ex_price_L= max(df['Low'][i], entry_price_L[i-1]*(1+ stop_profit))
                trade_ret_L= ex_price_L/ey_price_L -1
                exit_type= 'STOP_PROFIT'
                ey_price_L= np.nan
                trade_summary.append([model_position[-1], n_days_trade_L+ 1, trade_ret_L])
                
            elif (model_position[i-1]== -1) and (df['Low'][i]<= entry_price_S[i-1]*(1- stop_profit)):
                print('stop_profit_S', i)
                pos= 0             
                ex_price_S= min(df['High'][i], entry_price_S[i-1]*(1- stop_profit))
                trade_ret_S= -ex_price_S/ey_price_S +1
                exit_type= 'STOP_PROFIT'
                ey_price_S= np.nan
                trade_summary.append([model_position[-1], n_days_trade_S+ 1, trade_ret_S])
                
############################################
### Stop Loss 
############################################           
        if stop_loss:
            
            if (model_position[i-1]== 1) and (df['Low'][i]<= entry_price_L[i-1]*(1- stop_loss)):
                print('stop_loss_L', i)
                pos= 0               
                ex_price_L= min(df['High'][i], entry_price_L[i-1]*(1- stop_loss))
                trade_ret_L= ex_price_L/ey_price_L -1
                exit_type= 'STOP_LOSS'
                ey_price_L= np.nan
                trade_summary.append([model_position[-1], n_days_trade_L+ 1, trade_ret_L])
                
            elif (model_position[i-1]== -1) and (df['High'][i]>= entry_price_S[i-1]*(1+ stop_loss)):
                print('stop_loss_S', i)
                pos= 0                
                ex_price_S= max(df['Low'][i], entry_price_S[i-1]*(1+ stop_loss))
                trade_ret_S= -ex_price_S/ey_price_S +1
                exit_type= 'STOP_LOSS'
                ey_price_S= np.nan
                trade_summary.append([model_position[-1], n_days_trade_S+ 1, trade_ret_S])

############################################
### Signaux Exit Position
############################################         
        if df['EXIT_LONG'][i] and model_position[i-1]== 1 and pos!=0:
           pos= 0           
           ex_price_L= df['Close'][i]
           trade_ret_L= ex_price_L/ey_price_L -1
           exit_type= 'EXIT_LONG'
           ey_price_L= np.nan
           trade_summary.append([model_position[-1], n_days_trade_L+ 1, trade_ret_L])
           
        elif df['EXIT_SHORT'][i] and model_position[i-1]== -1 and pos!= 0:
           pos= 0           
           ex_price_S= df['Close'][i]
           trade_ret_S= -ex_price_S/ey_price_S +1
           exit_type= 'EXIT_SHORT'
           ey_price_S= np.nan
           trade_summary.append([model_position[-1], n_days_trade_S+ 1, trade_ret_S])
                
############################################
### Signaux Entry Position
############################################                   
        if (df['LONG'][i]) & (model_position[i-1]!= 1):
            pos= 1
            n_trades+= 1
            n_days_trade_L= 0
            ey_price_L= df['Close'][i]
            ex_price_L= np.nan
            if model_position[i-1]== -1:
                ex_price_S= df['Close'][i]
                # trade_ret_S= -ex_price_S/ey_price_S +1
            
        elif (df['SHORT'][i]) & (model_position[i-1]!= -1):
           pos= -1
           n_trades+= 1
           n_days_trade_S= 0
           ey_price_S= df['Close'][i]
           ex_price_S= np.nan
           if model_position[i-1]== 1:
                ex_price_L= df['Close'][i]
                # trade_ret_L= ex_price_L/ey_price_L -1
           
        print(i, pos, model_position[i-1])
        
        if (pos== 1) & (model_position[i-1]!= -1):
            ex_price_S= np.nan
            ey_price_S= np.nan
        if (pos== -1) & (model_position[i-1]!= 1):
            ex_price_L= np.nan
            ey_price_L= np.nan
        if (pos== 0) & (model_position[i-1]== 0):
            ex_price_S= np.nan
            ey_price_S= np.nan
            ex_price_L= np.nan
            ey_price_L= np.nan
        print(ex_price_L, ex_price_S)
        
            
        if i<i0:
            pos= 0
            ey_price_L= np.nan
            ey_price_S= np.nan
            ex_price_L= np.nan
            ex_price_S= np.nan
            trade_ret_L= np.nan
            trade_ret_S= np.nan

        if model_position[i-1]== 1:
            n_days_trade_L+= 1
            n_days_trade_S= 0
            
        if model_position[i-1]== -1:
            n_days_trade_S+= 1
            n_days_trade_L= 0
            
        if model_position[i-1]== 0:
            n_days_trade_L= 0
            n_days_trade_S= 0
            
        model_position= np.append(model_position, pos)
        entry_price_L= np.append(entry_price_L, ey_price_L)
        exit_price_L= np.append(exit_price_L, ex_price_L)
        entry_price_S= np.append(entry_price_S, ey_price_S)
        exit_price_S= np.append(exit_price_S, ex_price_S)
        trade_ret_all_L= np.append(trade_ret_all_L, trade_ret_L)
        trade_ret_all_S= np.append(trade_ret_all_S, trade_ret_S)
        n_days_L= np.append(n_days_L, n_days_trade_L)
        n_days_S= np.append(n_days_S, n_days_trade_S)
        
        
        print(trade_summary)
        
        if pos== model_position[-1]:
            day_ret= model_position[i-1]*(df.Close[i]/ df.Close[i-1] -1)
        elif model_position[i-1]== 0:
            day_ret= model_position[i-1]*(df.Close[i]/ ey_price_L)- 1
        else:
            day_ret= model_position[i-1]*(df.Close[i]/ df.Close[i-1]- 1)
            
        VL_ret= np.append(VL_ret, day_ret)
        
    df['position']= model_position
    df['entry_price_L']= entry_price_L
    df['exit_price_L']= exit_price_L
    df['entry_price_S']= entry_price_S
    df['exit_price_S']= exit_price_S
    df['n_days_L']= n_days_L
    df['n_days_S']= n_days_S
    df['VL_ret']= VL_ret
    df['VL_cum']= df['VL_ret'].cumsum(axis= 0)
    
    trade_stat= pd.DataFrame(trade_summary, columns=['pos', 'n_days', 'tot_ret'])
    trade_stat['Win_Loss']= trade_stat['tot_ret'].apply(lambda x: 'Loss' if x<0 else 'Win')
    trade_stat['Win_Loss']= trade_stat['Win_Loss'].apply(str)
    trade_stat['ticker']= ticker
    trade_statistics= trade_stat.groupby(['pos', 'Win_Loss']).agg(['count', 'mean','max', 'min'])
    
    return df, trade_stat, trade_statistics
############################################################################################################ 
####  APPLY STRATEGY
############################################################################################################     

# tickers= 'AAPL'
# tickers= ['AAPL', 'ISF.L', 'MC.PA', 'CAT']
# tickers= ['MC.PA', 'TTE.PA', 'ASML.AS', 'BNP.PA', 'G.MI', 'LHA.DE', '7203.T', 'IBM', 'GOOG']
# start_date= '2021-01-01'
# end_date= '2022-08-31'

# #  Strategy Parameters
# strategy= strategy_Bout
# n_up= 15
# n_down= 11
# n_shift= 0
# # i0= max(n_up, n_down)
# param= {'n_up': n_up, 'n_down': n_down, 'n_shift': n_shift}  # définir les param en dict
# i0= 0

# stop_loss= 0.03
# stop_profit= 0.06

# # Summary DataFrames
# VL= pd.DataFrame([])
# trade_stat_global= pd.DataFrame([])

# for ticker in tickers:
#     df= get_stock_data(ticker, start_date, end_date)
#     df_HLC= df[['High', 'Low', 'Close']]
    
#     # n_up, n_down= 21, 15
#     u= signal_strategy(df_HLC, start_date, end_date, strategy, **param)
    
    
#     v= run_strategy(u, i0= i0, stop_loss= stop_loss, stop_profit= stop_profit)
#     VL_ticker= v[0]['VL_cum']
#     trade_stat= v[1]
    
#     VL=pd.concat([VL, VL_ticker], axis= 1)
#     VL= VL.fillna(method= 'ffill')
#     trade_stat_global= pd.concat([trade_stat_global, trade_stat], axis= 0)
# # on garde le dernier ticker pour Excel
# v[0].to_excel('C:/Python_test/x1.xlsx', sheet_name= 'B')
# ############################################################################################################ 
# ####  BACKTEST 
# ############################################################################################################   

# VL_global= VL.mean(axis= 1)
# VLs= pd.concat([VL, VL_global], axis= 1)
# tickers_col= tickers.copy()
# tickers_col.append('VL_global')
# VLs.columns= tickers_col

# VLs.plot()
# plt.show()

# backtest_duration= VL_global.shape[0]/ 252
# trade_statistics_global= trade_stat_global.groupby(['pos', 'Win_Loss']).agg(['count',\
#                                                                             'mean','max', 'min'])
# trade_statistics_global= trade_statistics_global.reset_index()
# trade_statistics_global.columns= ['pos', 'Win_Loss','N_trades', 'Avg_ndays', 'Max_ndays', 'Min_ndays', 'nCount',\
# 'Avg_ret', 'Max_Ret', 'Min_ret']
# trade_statistics_global.drop('nCount', inplace= True, axis= 1)

# tot_number_trades= trade_statistics_global.N_trades.sum()
# win_ratio= trade_statistics_global[trade_statistics_global.Win_Loss== 'Win'].N_trades.sum()/ \
#                     tot_number_trades
                    
# temp_stat= trade_statistics_global[['Win_Loss', 'N_trades', 'Avg_ndays', 'Avg_ret']]

# avg_ret= temp_stat.N_trades* temp_stat.Avg_ret
# avg_ret= avg_ret.sum()/ tot_number_trades
# avg_ndays= temp_stat.N_trades* temp_stat.Avg_ndays
# avg_ndays= avg_ndays.sum()/ tot_number_trades

# temp_stat_win= temp_stat[temp_stat.Win_Loss== 'Win']

# avg_win_ret= temp_stat_win.N_trades* temp_stat.Avg_ret
# avg_win_ret= avg_win_ret.sum()/ temp_stat_win.N_trades.sum()
# avg_win_ndays= temp_stat_win.N_trades* temp_stat.Avg_ndays
# avg_win_ndays= avg_win_ndays.sum()/ temp_stat_win.N_trades.sum()

# temp_stat_loss= temp_stat[temp_stat.Win_Loss== 'Loss']

# avg_loss_ret= temp_stat_loss.N_trades* temp_stat.Avg_ret
# avg_loss_ret= avg_loss_ret.sum()/ temp_stat_loss.N_trades.sum()
# avg_loss_ndays= temp_stat_loss.N_trades* temp_stat.Avg_ndays
# avg_loss_ndays= avg_loss_ndays.sum()/ temp_stat_loss.N_trades.sum()

# VL_global_DD= VL_global- VL_global.cummax()
# VL_maxDD= np.min(VL_global_DD)

# print( f"########## Statistics ############ \n"
#       f"Average return: {avg_ret: .2%} \nWin ratio : {win_ratio: .1%} \n"
#       f"Win_return = {avg_win_ret: .2%} \n"
#       f"Loss_return  = {avg_loss_ret: .2%} \n"
#       f"Max_DrawDown : {VL_maxDD: .2%}")

############################################################################################################ 
####  ORDERS
############################################################################################################   

############################################################################################################ 
####  REGIME Function
############################################################################################################ 
## Cacul d'un target basé sur l'idée d'atteindre un objectif ER avec un risque de perte inférieure à ML (Max Loss) 

  
