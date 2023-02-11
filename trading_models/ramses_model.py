from trading_models.base import SimpleTradingModel
from strategies.breakout_strategy import compute_breakout_signals
from strategies.rsi_strategy import compute_rsi, compute_rsi_signals
from pandas import DataFrame
import numpy as np
import enum

class State(str, enum.Enum):
    EXIT_LONG_SUR_SIGNAL="EXIT_LONG_SUR_SIGNAL"
    EXIT_LONG_SUR_STOP_LOSS="EXIT_LONG_SUR_STOP_LOSS"
    EXIT_LONG_SUR_STOP_PROFIT="EXIT_LONG_SUR_STOP_PROFIT"
    EXIT_SHORT_SUR_SIGNAL="EXIT_SHORT_SUR_SIGNAL"
    EXIT_SHORT_SUR_STOP_LOSS="EXIT_SHORT_SUR_STOP_LOSS"
    EXIT_SHORT_SUR_STOP_PROFIT="EXIT_SHORT_SUR_STOP_PROFIT"
    LONG="LONG"
    LONG_AND_EXIT_SHORT_SUR_SIGNAL="LONG_AND_EXIT_SHORT_SUR_SIGNAL"
    LONG_AND_EXIT_SHORT_SUR_STOP_LOSS="LONG_AND_EXIT_SHORT_SUR_STOP_LOSS"
    LONG_AND_EXIT_SHORT_SUR_STOP_PROFIT="LONG_AND_EXIT_SHORT_SUR_STOP_PROFIT"
    SHORT="SHORT"
    SHORT_AND_EXIT_LONG_SUR_SIGNAL="SHORT_AND_EXIT_LONG_SUR_SIGNAL"
    SHORT_AND_EXIT_LONG_SUR_STOP_LOSS="SHORT_AND_EXIT_LONG_SUR_STOP_LOSS"
    SHORT_AND_EXIT_LONG_SUR_STOP_PROFIT="SHORT_AND_EXIT_LONG_SUR_STOP_PROFIT"

    NONE="NONE"


class RamsesModel(SimpleTradingModel):

    @classmethod
    def compute_features(cls, df) -> DataFrame:
        rsi_window = 14
        return DataFrame({
            'rsi': compute_rsi(df, rsi_window),
        })

    @classmethod
    def compute_signals(cls, df, features: DataFrame):
        return DataFrame({
            'rsi':compute_rsi_signals(features['rsi']),
            'breakout':compute_breakout_signals(df)
        })

    @classmethod
    def _get_exit_price(cls, model_positions, is_exit_long):
        reversed_model_positions = model_positions[::-1]
        expected_position = 1 if is_exit_long else -1 # Implicitly is exit_short then
        for i in range(len(model_positions)):
            if reversed_model_positions[i][0] != expected_position:
                return len(model_positions) - i
        return None

    @classmethod
    def _get_position_state(cls, df, stop_loss, stop_profit):        
        model_positions = [(0, None, None, None)]
        for i in range(1, df.shape[0]):
            last_position, last_entry_price, _, _ = model_positions[i-1]
            price = last_entry_price or 0
            
            if (df['LONG'][i] and last_position != 1):
                model_positions.append((1, df['Close'][i], None, None))
            elif (df['SHORT'][i] and last_position != -1):
                model_positions.append((-1, df['Close'][i], None, None))
            elif (df['EXIT_LONG'][i] or df['EXIT_SHORT'][i]):
                model_positions.reverse()
                model_positions.append((0, None, df['Close'][i], cls._get_exit_price(model_positions, df['EXIT_LONG'][i])))
            elif last_position == 1 and (
                df['Low'][i]<= price*(1 - stop_loss) or df['High'][i] > price*(1 + stop_profit)
            ):
                model_positions.append((0, None, None, None))
            elif last_position == -1 and (
                df['High'][i] > price*(1 + stop_loss) or df['Low'][i]<= price*(1- stop_profit)
            ):
                model_positions.append((0, None, None, None))
            else:
                model_positions.append((last_position, last_entry_price, None, None))

        state_list = []
        for i in range(1, df.shape[0]):
            last_position, last_price, _, _ = model_positions[i-1]
            position, entry_price, exit_price, nb_days = model_positions[i]
            is_short = last_position == -1
            is_long = last_position == 1
            price = entry_price or 0
            print(f'last_price  {last_price}  {entry_price}')
            state = State.NONE
            if is_long and df['EXIT_LONG'][i]:
                state= State.EXIT_LONG_SUR_SIGNAL if not df['SHORT'][i] else State.SHORT_AND_EXIT_LONG_SUR_SIGNAL
            elif is_long and df['Low'][i]<= price*(1 - stop_loss):
                state=  State.EXIT_LONG_SUR_STOP_LOSS if not df['SHORT'][i] else State.SHORT_AND_EXIT_LONG_SUR_STOP_LOSS
            elif is_long and df['High'][i] > price*(1 + stop_profit):
                state=  State.EXIT_LONG_SUR_STOP_PROFIT if not df['SHORT'][i] else State.SHORT_AND_EXIT_LONG_SUR_STOP_PROFIT
            elif is_short and df['EXIT_SHORT'][i]:
                state=  State.EXIT_SHORT_SUR_SIGNAL if not df['LONG'][i] else State.LONG_AND_EXIT_SHORT_SUR_SIGNAL
            elif is_short and df['High'][i] > price*(1 + stop_loss):
                    state=  State.EXIT_SHORT_SUR_STOP_LOSS if not df['LONG'][i] else State.LONG_AND_EXIT_SHORT_SUR_STOP_LOSS
            elif is_short and df['Low'][i]<= price*(1- stop_profit):
                    state=  State.EXIT_SHORT_SUR_STOP_PROFIT if not df['LONG'][i] else State.LONG_AND_EXIT_SHORT_SUR_STOP_PROFIT
            elif position == 1:
                state=  State.LONG
            elif position == -1:
                state=  State.SHORT
            state_list.append({
                'position': position,
                'entry_price': entry_price if state in [State.LONG, State.SHORT, State.NONE] else model_positions[i-2][1],
                'exit_price':  exit_price,
                'state': state,
                'nb_days': nb_days
            })
        return state_list




            # if df['EXIT_LONG'][i] and is_long:
            #     state = State.EXIT_LONG_SUR_SIGNAL
            # if df['EXIT_LONG'][i] and df['Low'][i]<= entry_price*(1 + stop_loss):
            #     state = State.EXIT_LONG_SUR_STOP_LOSS
            # if df['EXIT_LONG'][i] and df['High'][i] > entry_price*(1 - stop_profit):
            #     state = State.EXIT_LONG_SUR_STOP_PROFIT
            # if df['SHORT'] and df['EXIT_LONG'][i] and is_long:
            #     state = State.SHORT_AND_EXIT_LONG_SUR_SIGNAL
            # if df['SHORT'] and df['EXIT_LONG'][i] and df['Low'][i]<= entry_price*(1 + stop_loss):
            #     state = State.SHORT_AND_EXIT_LONG_SUR_STOP_LOSS
            # if df['SHORT'] and df['EXIT_LONG'][i] and df['High'][i] > entry_price*(1 - stop_profit):
            #     state = State.SHORT_AND_EXIT_LONG_SUR_STOP_PROFIT
            # if df['EXIT_SHORT'][i] and is_short:
            #     state = State.EXIT_SHORT_SUR_SIGNAL
            # if df['EXIT_SHORT'][i] and df['High'][i] > entry_price*(1 - stop_profit):
            #     state = State.EXIT_SHORT_SUR_STOP_LOSS
            # if df['EXIT_SHORT'][i] and df['Low'][i]<= entry_price*(1- stop_profit):
            #     state = State.EXIT_SHORT_SUR_STOP_PROFIT
            # if df['LONG'] and df['EXIT_SHORT'][i] and is_short:
            #     state = State.LONG_AND_EXIT_SHORT_SUR_SIGNAL
            # if df['LONG'] and df['EXIT_SHORT'][i] and df['High'][i] > entry_price*(1 - stop_profit):
            #     state = State.LONG_AND_EXIT_SHORT_SUR_STOP_LOSS
            # if df['LONG'] and df['EXIT_SHORT'][i] and df['Low'][i]<= entry_price*(1- stop_profit):
            #     state = State.LONG_AND_EXIT_SHORT_SUR_STOP_PROFIT
            # if is_long and df['LONG']:
            #     state = State.LONG
            # if is_short and df['SHORT']:
            #     state = State.SHORT

    @classmethod
    def run_strategy(signal_df, stop_loss= None, stop_profit= None, regime= None):
        # il est bon de séparer la stratégie de Stop-Loss de celle du signal, afin de pouvoir tester plusieurs 
        # stratégies de stop-loss
        # l objectif de la fonction est de fournir une position, un prix d entrée un prix de sortie et des stats
        df= signal_df.copy()
        first_date = 0 # first_date est la première date de run de la strategy
        
        ## variables quotidiennes
        pos= 0
        entry_price_L= np.nan
        entry_price_S= np.nan
        exit_price_L= np.nan
        exit_price_S= np.nan
        n_trades= 0
        n_days_trade_L= 0
        n_days_trade_S= 0
        daily_return= 0
        ## variables discontinues
        trade_return_L= np.nan
        trade_return_S= np.nan
        trade_summary= []
        ## variables cumulées
        model_position= [0]
        entry_price_L= np.nan
        entry_price_S= np.nan
        exit_price_L= np.nan
        exit_price_S= np.nan
        trade_return_all_L= 0
        trade_return_all_S= 0
        n_days_L= 0
        n_days_S= 0
        VL_ret= [0]


            

        for i in range(1, df.shape[0]):
            last_position = model_position[-1]
            is_long = last_position == 1
            is_short = last_position == -1

            ############################################
            ### Stop Profit 
            ############################################
            if stop_profit:
                stop_profit_price = entry_price_L[i-1]*(1+ stop_profit)
                if is_long and df['High'][i] > stop_profit_price:
                    # exit_price_L= max(df['Low'][i], stop_profit_price)
                    # trade_return_L= exit_price_L/entry_price_L -1

                    # exit_type= 'STOP_PROFIT'
                    pos= 0                
                    # entry_price_L= np.nan
                    # trade_summary.append([last_position, n_days_trade_L+ 1, trade_return_L])
                    
                elif is_short and df['Low'][i]<= entry_price_S[i-1]*(1- stop_profit):
                    # exit_price_S= min(df['High'][i], entry_price_S[i-1]*(1- stop_profit))
                    # trade_return_S= -exit_price_S/entry_price_S +1

                    # exit_type= 'STOP_PROFIT'
                    pos= 0             
                    # entry_price_S= np.nan
                    # trade_summary.append([last_position, n_days_trade_S+ 1, trade_return_S])
                    
            ############################################
            ### Stop Loss 
            ############################################
                       
            if stop_loss:
                stop_loss_price = entry_price_L[i-1]*(1- stop_loss)
                if is_long and df['Low'][i]<= stop_loss_price:
                    # exit_price_L= min(df['High'][i], stop_loss_price)
                    # trade_return_L= exit_price_L/entry_price_L -1
                
                    # exit_type= 'STOP_LOSS'
                    pos= 0               
                    # entry_price_L= np.nan
                    # trade_summary.append([last_position, n_days_trade_L+ 1, trade_return_L])
                    
                elif is_short and df['High'][i]>= entry_price_S[i-1]*(1+ stop_loss):
                    # exit_price_S= max(df['Low'][i], entry_price_S[i-1]*(1+ stop_loss))
                    # trade_return_S= -exit_price_S/entry_price_S +1

                    # exit_type= 'STOP_LOSS'
                    pos= 0                
                    # entry_price_S= np.nan
                    # trade_summary.append([last_position, n_days_trade_S+ 1, trade_return_S])

            ############################################
            ### Signaux Exit Position
            ############################################         
            if df['EXIT_LONG'][i] and last_position== 1 and pos != 0:
                pos= 0           
                # exit_price_L= df['Close'][i]
                # trade_return_L= exit_price_L/entry_price_L -1
                # exit_type= 'EXIT_LONG'
                # entry_price_L= np.nan
                # trade_summary.append([last_position, n_days_trade_L+ 1, trade_return_L])
            
            elif df['EXIT_SHORT'][i] and last_position== -1 and pos!= 0:
                pos= 0           
                # exit_price_S= df['Close'][i]
                # trade_return_S= -exit_price_S/entry_price_S +1
                # exit_type= 'EXIT_SHORT'
                # entry_price_S= np.nan
                # trade_summary.append([last_position, n_days_trade_S+ 1, trade_return_S])
                    
            ############################################
            ### Signaux Entry Position
            ############################################                   
            if (df['LONG'][i]) & (last_position!= 1):
                pos = 1
                n_trades+= 1
                n_days_trade_L= 0
                entry_price_L= df['Close'][i]
                exit_price_L= np.nan
                if last_position== -1:
                    exit_price_S= df['Close'][i]
                    # trade_return_S= -exit_price_S/entry_price_S +1
                
            elif (df['SHORT'][i]) & (last_position!= -1):
                pos= -1
                n_trades+= 1
                n_days_trade_S= 0
                entry_price_S= df['Close'][i]
                exit_price_S= np.nan
                if last_position== 1:
                        exit_price_L= df['Close'][i]
                        # trade_return_L= exit_price_L/entry_price_L -1
            
            if (pos== 1) & (last_position!= -1):
                exit_price_S= np.nan
                entry_price_S= np.nan
            if (pos== -1) & (last_position!= 1):
                exit_price_L= np.nan
                entry_price_L= np.nan
            if (pos== 0) & (last_position== 0):
                exit_price_S= np.nan
                entry_price_S= np.nan
                exit_price_L= np.nan
                entry_price_L= np.nan
            
                
            if i<first_date:
                pos= 0
                entry_price_L= np.nan
                entry_price_S= np.nan
                exit_price_L= np.nan
                exit_price_S= np.nan
                trade_return_L= np.nan
                trade_return_S= np.nan

            if last_position== 1:
                n_days_trade_L+= 1
                n_days_trade_S= 0
                
            if last_position== -1:
                n_days_trade_S+= 1
                n_days_trade_L= 0
                
            if last_position== 0:
                n_days_trade_L= 0
                n_days_trade_S= 0
                
            model_position= np.append(model_position, pos)
            entry_price_L= np.append(entry_price_L, entry_price_L)
            exit_price_L= np.append(exit_price_L, exit_price_L)
            entry_price_S= np.append(entry_price_S, entry_price_S)
            exit_price_S= np.append(exit_price_S, exit_price_S)
            trade_return_all_L= np.append(trade_return_all_L, trade_return_L)
            trade_return_all_S= np.append(trade_return_all_S, trade_return_S)
            n_days_L= np.append(n_days_L, n_days_trade_L)
            n_days_S= np.append(n_days_S, n_days_trade_S)
            
            if pos== last_position:
                daily_return= last_position*(df.Close[i]/ df.Close[i-1] -1)
            elif last_position== 0:
                daily_return= last_position*(df.Close[i]/ entry_price_L)- 1
            else:
                daily_return= last_position*(df.Close[i]/ df.Close[i-1]- 1)
                
            VL_ret= np.append(VL_ret, daily_return)
            
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
        # trade_stat['ticker']= ticker
        trade_statistics= trade_stat.groupby(['pos', 'Win_Loss']).agg(['count', 'mean','max', 'min'])
        
        return df, trade_stat, trade_statistics


    @classmethod
    def run_strategies(cls, features, signals):
        pass

    @classmethod
    def run_meta_strategy(cls, orders, features, signals):
        pass

    @classmethod
    def compute_stats(cls, orders, features, signals):
        pass

    # @classmethod
    # def compute_signal(cls, data)-> int:
    #     df_strategy= strategy(df, **kwargs)
    #     signal_df= df_strategy[(df_strategy.index >= start_date) & (df_strategy.index<= end_date)]
    #     return signal_df


    @classmethod
    def apply_stop_loss_policy(cls):
        '''
        Apply stop loss policy
        '''
        pass

    @classmethod
    def apply_stop_profit_policy(cls):
        '''
        Apply stop profit policy
        '''
        pass

    @classmethod
    def apply_policies(cls, signal):
        '''
        Apply stop loss and stop profit policies
        '''
        pass

