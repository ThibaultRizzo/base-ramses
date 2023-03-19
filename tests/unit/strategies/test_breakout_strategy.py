from strategies.breakout_strategy import compute_breakout_signals
from tests.datasets.dataset_generator import get_ohlc_dataframe
from datetime import datetime
from utils.testing import compare_item, compare_list

def test_compute_breakout_signals():
    df = get_ohlc_dataframe('1h', datetime(2022, 3,1), datetime(2022, 3,15))
    print('compute_breakout_signals')
    print(compute_breakout_signals(df))
    assert False
