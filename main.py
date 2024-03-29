"""
Main module
"""
from typing import List

from models import TradingModel, TradingModelOrder

from .broker import ExecutedOrder, send_orders


def retrieve_trading_models() -> List[TradingModel]:
    """
    Fetch all active trading models which need to be executed for the given activation time
    """
    pass


def pull_tickers_from_models(models: List[TradingModel]):
    """
    1. Get all instruments linked to given models
    2. Fetch them if necessary and persist them
    """
    pass


def build_portfolio(orders: List[TradingModelOrder]):
    """
    Build portfolio while taking current portfolio and computed risk
    """
    pass


def compute_post_thread_stats(orders: List[ExecutedOrder]):
    """
    Send orders to broker
    """
    pass


def main():
    """
    This script will be executed every business hour
    """
    # 1. Retrieve models to be computed
    models = retrieve_trading_models()

    # 2. Pull tickers
    pull_tickers_from_models(models)
    ## Fix missing data

    # 3. Execute models
    orders = []
    for model in models:
        orders.extend(model.execute())

    # 4. Build portfolio
    orders_to_pass = build_portfolio(orders)

    # 5. Call broker
    executed_orders = send_orders(orders_to_pass)

    # 6. Compute Post Thread Stats
    compute_post_thread_stats(executed_orders)
