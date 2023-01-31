from strategies.rsi_strategy import compute_rsi, compute_rsi_signals
from tests.datasets.dataset_generator import get_ohlc_dataframe
from datetime import datetime
from utils.testing import compare_item, compare_list

def test_compute_rsi():
    df = get_ohlc_dataframe('1h', datetime(2022, 3,1), datetime(2022, 3,15))
    print('test_compute_rsi')
    print(compute_rsi(df))
    assert False

def test_compute_rsi_signals():
    df = get_ohlc_dataframe('1h', datetime(2022, 3,1), datetime(2022, 3,15))
    print('compute_rsi_signals')
    data = compute_rsi(df)
    print(compute_rsi_signals(data))
    assert False
