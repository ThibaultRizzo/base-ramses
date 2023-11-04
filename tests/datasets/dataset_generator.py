from datetime import datetime, time, timedelta
import random
from zoneinfo import ZoneInfo

from pandas import DataFrame, DatetimeIndex


def get_ohlc_dataframe(
    interval,
    start,
    end=None,
):
    is_hourly = interval and interval == "1h"
    datetime_delta = end - start
    if is_hourly:
        datetime_index = [
            datetime.combine(start.date(), time(hour=hour, minute=30), tzinfo=ZoneInfo("America/New_York"))
            + timedelta(days=day + 1)
            for day in range(datetime_delta.days - 1)
            for hour in range(9, 16)
        ]
    else:
        datetime_index = [start + timedelta(days=day + 1) for day in range(datetime_delta.days - 1)]
    dt_size = len(datetime_index)

    return DataFrame(
        {
            "Open": [random.random() * 100 for _ in range(dt_size)],
            "High": [random.random() * 100 for _ in range(dt_size)],
            "Low": [random.random() * 100 for _ in range(dt_size)],
            "Close": [random.random() * 100 for _ in range(dt_size)],
            "Adj Close": [random.random() * 100 for _ in range(dt_size)],
            "Volume": [random.random() * 100 for _ in range(dt_size)],
        },
        index=DatetimeIndex(datetime_index),
    )
