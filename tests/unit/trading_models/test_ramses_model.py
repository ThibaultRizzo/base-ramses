from tests.datasets.dataset_generator import get_ohlc_dataframe
from datetime import datetime
from trading_models.ramses_model import RamsesModel, State
from pandas import DataFrame, DatetimeIndex
from utils.testing import compare_item, compare_list
from strategies.rsi_strategy import get_rsi_strategy

def test_get_number_of_days_in_position():
    model_positions = [
        (1, 12, None, 3),
        (1, 12, None, 3),
    ]
    assert RamsesModel._get_number_of_days_in_position(model_positions, is_exit_long=True)

    model_positions = [
        (),
    ]
    assert RamsesModel._get_exit_price(model_positions, is_exit_long=False)

def test_get_model_position():
    df = DataFrame(
        {
            # 'Open': [1,2,3,4],
            'High': [1,2,2,4,4],
            'Low': [1,2,2,4,4],
            'Close': [1,2,3,4,4],
            # 'Adj Close': [1,2,3,4],
            # 'Volume': [1,2,3,4],
            'LONG': [False,True,False,False,False],
            'SHORT': [False,False,False,False,False],
            'EXIT_LONG': [False,False,False,True,False],
            'EXIT_SHORT': [False,False,False,False,False],
        },
        index=DatetimeIndex([
            datetime(2022, 1,1),
            datetime(2022, 1,2),
            datetime(2022, 1,3),
            datetime(2022, 1,4),
            datetime(2022, 1,5)
        ])
    )
    compare_list([
        (1,2,3,4,5)
    ], RamsesModel._get_model_position(
        df, 
        0.05,
        0.02
    ))

def test_ramses_model_compute_signals():
    df = get_ohlc_dataframe('1h', datetime(2022, 3,1), datetime(2022, 3,15))
    print(RamsesModel.compute_signals(
        df, RamsesModel.compute_features(df), {
            'rsi': get_rsi_strategy(
                n= list(range(9,22,3)),
                n_seuil= list(range(15,31,5)),
                n_shift= [0,1]
            )
        }
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
    