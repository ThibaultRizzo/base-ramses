# -*- coding: utf-8 -*-
"""
Created on Sun Jul 31 18:19:30 2022

@author: 33688
"""

import RAMSES_lib as RMSlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import product

############################################################################################################ 
####  APPLY STRATEGY
############################################################################################################     
## On crée un fichier de statistiques permettant d'observer sur un échantillon de tickers
## l'application de multiples stratégies avec de multiples paramétrages}
#####################################################
#######    Tickers Sample
tickers= ['AAPL', 'GOOG']
# tickers= ['AAPL', 'ISF.L', 'MC.PA', 'CAT']
# tickers= ['MC.PA', 'TTE.PA', 'ASML.AS', 'BNP.PA', 'G.MI', 'LHA.DE', '7203.T', 'IBM', 'GOOG']
#####################################################
#######    Période de calcul des statistics
##  le buffer de dates permet d'avoir un modèle pleinement opérationnel dès la strat_date
start_date= '2021-01-01'
end_date= '2022-08-31'
#####################################################
####### Stratégies choisies
sample_strategies= [RMSlib.strategy_Bout, RMSlib.strategy_RSI]
#####################################################
####### Paramètres des stratégies
##  pour chaque stratégie, on crée un jeu de paramètres
strat_0= {'strat': sample_strategies[0], 
     'param': {
         'n_up': [15, 25, 35],
         'n_down': [11,21,31],
         'n_shift': [0,1]
             }
     }
strat_1= {'strat': sample_strategies[1], 
     'param': {
         'n': [i for i in range(9,22,3)],
         'n_seuil': [i for i in range(15,31,5)],
         'n_shift': [0,1]
             }
     }
## les stratégies peuvent donc se résumer à: lister les strat avec param
strategies=[strat_0, strat_1]
## Pour une stratégie donnée:  
# strategy= RMSlib.strategy_Bout
# n_up= 15
# n_down= 11
# n_shift= 0
# param= {'n_up': n_up, 'n_down': n_down, 'n_shift': n_shift}  # définir les param en dict
# i0= 0
# stop_loss= 0.03
# stop_profit= 0.06
#####################################################
####### Approche multi-paramètres pour différentes Stratégies
for strategy in strategies:
    
    strat= strategy['strat']
    param_strat= strategy['param']
    
    param_name= []
    param_list= []
    
    for p_s in param_strat:
        param_name.append(p_s)
        param_list.append(param_strat[p_s])
        
    ## on génère la liste des dictionnaires qui servent dans le paramétrage
    param_dict_list= [dict(zip(param_name, param)) for param in list(product(*param_list))]
    param= param_dict_list[0]
    i0= 0
    stop_loss= 0.03
    stop_profit= 0.06
    # Summary DataFrames
    VL= pd.DataFrame([])
    trade_stat_global= pd.DataFrame([])
    # Columns title
    strategy_name= str(strat).split(' ')[1]  +str(param)
    
    for ticker in tickers:
        df= RMSlib.get_stock_data(ticker, start_date, end_date)
        df_HLC= df[['High', 'Low', 'Close']]
        
        # n_up, n_down= 21, 15
        u= RMSlib.signal_strategy(df_HLC, start_date, end_date, strat, **param)
        
        v= RMSlib.run_strategy(ticker, u, i0= i0, stop_loss= stop_loss, stop_profit= stop_profit)
        VL_ticker= v[0]['VL_cum']
        trade_stat= v[1]
        trade_stat['strategy']= strategy_name
        
        VL=pd.concat([VL, VL_ticker], axis= 1)
        VL= VL.fillna(method= 'ffill')
        trade_stat_global= pd.concat([trade_stat_global, trade_stat], axis= 0)
# on garde le dernier ticker pour Excel
# v[0].to_excel('C:/Python_test/x1.xlsx', sheet_name= 'B')
############################################################################################################ 
####  BACKTEST 
############################################################################################################   

    VL_global= VL.mean(axis= 1)
    VLs= pd.concat([VL, VL_global], axis= 1)
    tickers_col= tickers.copy()
    tickers_col.append('VL_global')
    VLs.columns= tickers_col
    
    VLs.plot()
    plt.show()
    
    backtest_duration= VL_global.shape[0]/ 252
    trade_statistics_global= trade_stat_global.groupby(['pos', 'Win_Loss']).agg(['count',\
                                                                                'mean','max', 'min'])
    trade_statistics_global= trade_statistics_global.reset_index()
    trade_statistics_global.columns= ['pos', 'Win_Loss','N_trades', 'Avg_ndays', 'Max_ndays', 'Min_ndays', 'nCount',\
    'Avg_ret', 'Max_Ret', 'Min_ret']
    trade_statistics_global.drop('nCount', inplace= True, axis= 1)
    
    tot_number_trades= trade_statistics_global.N_trades.sum()
    win_ratio= trade_statistics_global[trade_statistics_global.Win_Loss== 'Win'].N_trades.sum()/ \
                        tot_number_trades
                        
    temp_stat= trade_statistics_global[['Win_Loss', 'N_trades', 'Avg_ndays', 'Avg_ret']]
    
    avg_ret= temp_stat.N_trades* temp_stat.Avg_ret
    avg_ret= avg_ret.sum()/ tot_number_trades
    avg_ndays= temp_stat.N_trades* temp_stat.Avg_ndays
    avg_ndays= avg_ndays.sum()/ tot_number_trades
    
    temp_stat_win= temp_stat[temp_stat.Win_Loss== 'Win']
    
    avg_win_ret= temp_stat_win.N_trades* temp_stat.Avg_ret
    avg_win_ret= avg_win_ret.sum()/ temp_stat_win.N_trades.sum()
    avg_win_ndays= temp_stat_win.N_trades* temp_stat.Avg_ndays
    avg_win_ndays= avg_win_ndays.sum()/ temp_stat_win.N_trades.sum()
    
    temp_stat_loss= temp_stat[temp_stat.Win_Loss== 'Loss']
    
    avg_loss_ret= temp_stat_loss.N_trades* temp_stat.Avg_ret
    avg_loss_ret= avg_loss_ret.sum()/ temp_stat_loss.N_trades.sum()
    avg_loss_ndays= temp_stat_loss.N_trades* temp_stat.Avg_ndays
    avg_loss_ndays= avg_loss_ndays.sum()/ temp_stat_loss.N_trades.sum()
    
    VL_global_DD= VL_global- VL_global.cummax()
    VL_maxDD= np.min(VL_global_DD)
    
    print( f"########## Statistics ############ \n"
          f"Tickers:  {tickers} \n"
          f"Average return: {avg_ret: .2%} \nWin ratio : {win_ratio: .1%} \n"
          f"Win_return = {avg_win_ret: .2%} \n"
          f"Loss_return  = {avg_loss_ret: .2%} \n"
          f"Max_DrawDown : {VL_maxDD: .2%}")
    
    ############################################################################################################ 
    ####  ORDERS
    ############################################################################################################   
    
     
    
      
