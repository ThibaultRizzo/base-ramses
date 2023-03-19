from strategies.rsi_strategy import compute_rsi_signals, get_rsi_strategy
from tests.datasets.dataset_generator import get_ohlc_dataframe
from datetime import datetime
from utils.testing import compare_item, compare_list

def test_compute_rsi_signals():
    df = get_ohlc_dataframe('1h', datetime(2022, 3,1), datetime(2022, 3,15))
    compute_rsi = get_rsi_strategy(12, 1, 0)
    print(compute_rsi(df))
    assert False
