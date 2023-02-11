from dataclasses import dataclass
from pandas import DataFrame
from crud.trading_model_crud import TradingModelCrud
from models import TradingModel, HourlyPriceTimeseries
from typing import Dict, List

@dataclass
class BaseTradingModel:

    @classmethod
    def load_data(cls, trading_model: TradingModel)-> DataFrame:
        '''
        Recupere l'ensemble des instruments necessaires sur les intervalles definis
        '''
        return TradingModelCrud.get_instrument_timeseries(trading_model.id)

    @classmethod
    def execute(cls, trading_model: TradingModel):
        pass

@dataclass
class SimpleTradingModel(BaseTradingModel):

    @classmethod
    def compute_features(cls, data: DataFrame):
        pass

    @classmethod
    def compute_signals(cls, data: DataFrame, features):
        pass

    @classmethod
    def run_strategies(cls, features, signals):
        pass

    @classmethod
    def run_meta_strategy(cls, orders, features, signals):
        pass

    @classmethod
    def compute_stats(cls, orders, features, signals):
        pass

    @classmethod
    def execute(cls, trading_model: TradingModel):
        ticker_dict = cls.load_data(trading_model)
        order_list = []
        for ticker in ticker_dict:
            data = ticker_dict[ticker]
            features = cls.compute_features(data)
            feature_signals = cls.compute_signals(data, features)
            orders_to_pass = cls.run_strategies(features, feature_signals)
            orders_from_meta_strategy =  cls.run_meta_strategy(orders_to_pass, features, feature_signals)
            order_list = order_list.extend(orders_from_meta_strategy)
            cls.compute_stats(trading_model, order_list)
        return order_list

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

    @classmethod
    def run_strategy(cls, trading_model: TradingModel, data: Dict[str, List[HourlyPriceTimeseries]]):
        

        ## Data des ts
        ## A partir des data, calculer les features necessaires

        


        # Pour chaque strategie
        ## Pour chaque ticker
        #### Compute signal
        ###### Etant donne une strategie, emet un signal en fonction des ts
        #### Run strategy
        #### Compute stats
        #### Compute backtest infos ?
        signal = cls.compute_signal(data)
        return cls.apply_policies(signal)
