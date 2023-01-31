from tests.datasets.dataset_generator import get_ohlc_dataframe
from datetime import datetime
from trading_models.ramses_model import RamsesModel, State
from pandas import DataFrame, DatetimeIndex
from utils.testing import compare_item, compare_list


def test_ramses_model_compute_signals():
    df = get_ohlc_dataframe('1h', datetime(2022, 3,1), datetime(2022, 3,15))
    print(RamsesModel.compute_signals(
        df, RamsesModel.compute_features(df)
    ))

    assert False



def test_ramses_model_get_position_state():
    # 1.
    df = DataFrame(
        {
            'Open': [1,2,3,4],
            'High': [1,2,2,4],
            'Low': [1,2,2,4],
            'Close': [1,2,3,4],
            'Adj Close': [1,2,3,4],
            'Volume': [1,2,3,4],
            'LONG': [False,True,False,False,],
            'SHORT': [False,False,False,False,],
            'EXIT_LONG': [False,False,False,True,],
            'EXIT_SHORT': [False,False,False,False,],
        },
        index=DatetimeIndex([
            datetime(2022, 1,1),
            datetime(2022, 1,2),
            datetime(2022, 1,3),
            datetime(2022, 1,4)
        ])
    )
    compare_list([{
        'entry_price': 0,
        'position': 0,
        'state': State.LONG,
    }],RamsesModel._get_position_state(
        df,
        0.05,
        0.02
    ))

    #2.
    df = DataFrame(
        {
            'Open': [1,2,3,4, 5,6,7],
            'High': [1,2,3,3, 3,5,5],
            'Low': [1,2,3,4, 5,2, 1],
            'Close': [1,2,3,4, 5,6,7],
            'LONG': [False,False,True,False,False,False,False],
            'SHORT': [False,False,False,False,False,False,False],
            'EXIT_LONG': [False,False,False,False,False,False,False],
            'EXIT_SHORT': [False,False,False,False,False,False,False],
        },
        index=DatetimeIndex([
            datetime(2022, 1,1),
            datetime(2022, 1,2),
            datetime(2022, 1,3),
            datetime(2022, 1,4),
            datetime(2022, 1,5),
            datetime(2022, 1,6),
            datetime(2022, 1,7),
        ])
    )
    compare_list([
        State.NONE,
        State.LONG,
        State.LONG,
        State.LONG,
        State.EXIT_LONG_SUR_STOP_PROFIT,
        State.NONE,
    ],RamsesModel._get_position_state(
        df,
        0.5,
        0.5
    ))

    assert False
    