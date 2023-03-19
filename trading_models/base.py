from dataclasses import dataclass
from pandas import DataFrame
from crud.trading_model_crud import TradingModelCrud
from models import TradingModel, HourlyPriceTimeseries
from typing import Dict, List, Callable

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

StrategyCallable = Callable[[DataFrame], DataFrame]

@dataclass
class SimpleTradingModel(BaseTradingModel):

    @classmethod
    def execute(cls, trading_model: TradingModel):
        # Fetch timeseries for every ticker linked to the model, on the PERIOD and FREQUENCY on which i want to execute this model
        ticker_df = cls.load_data(trading_model)

        # Get configured strategy list (list of curried functions with fixed parameters)
        strategies = cls.get_strategies()

        order_list = []
        for ticker in ticker_df:
            df = ticker_df[ticker]
            # Compute list of features from ticker base raw data
            features_df = cls.compute_features(df)

            # Compute signal dataframe from raw data and features for each configured strategy
            # dataframe of N tickers over X dates and Y strategies with values -1, 0 or 1
            signals_df = cls.compute_signals(df, features_df, strategies)

            # Compute orders to send from signals dataframe
            # dataframe of N tickers over Y strategies with order list as value
            ticker_order_list = cls.compute_orders(signals_df)
            order_list = order_list.extend(ticker_order_list)

            # Compute stats for the orders to send
            cls.compute_stats(order_list)

        return order_list

            
        # for strategy in strategies:
        #     for ticker in ticker_df:
        #         df = ticker_df[ticker]
        #         features_df = cls.compute_features(df)
        #         signals_df = cls.compute_signals(df, features_df)
        #         orders_to_pass = cls.run_strategies(features_df, signals_df)
        #         orders_from_meta_strategy =  cls.run_meta_strategy(orders_to_pass, features, feature_signals)
        #         order_list = order_list.extend(orders_from_meta_strategy)
        #         cls.compute_stats(trading_model, order_list)
        # return order_list

    @classmethod
    def get_strategies(cls) -> Dict[str, StrategyCallable]:
        pass

    @classmethod
    def compute_features(cls, data: DataFrame):
        pass

    @classmethod
    def compute_signals(cls, data: DataFrame, features: DataFrame, strategies: Dict[str, StrategyCallable]) -> DataFrame:
        pass

    @classmethod
    def compute_orders(cls, signals_df: DataFrame)-> List[int]:
        pass

    @classmethod
    def run_strategies(cls, features_df: DataFrame, signals_df: DataFrame) -> List[int]:
        pass

    @classmethod
    def run_meta_strategy(cls, orders, features, signals):
        pass

    @classmethod
    def compute_stats(cls, orders, features, signals):
        pass

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
