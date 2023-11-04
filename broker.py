"""
Broker module
"""
from typing import List

from models import TradingModelOrder


class ExecutedOrder:
    pass


def send_orders(orders: List[TradingModelOrder]) -> List[ExecutedOrder]:
    """
    Send orders to broker
    """
    pass
