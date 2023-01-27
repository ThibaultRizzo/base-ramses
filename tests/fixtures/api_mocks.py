import pytest
import yfinance
import pandas as pd
from datetime import datetime, timedelta, time, timezone
import random
from zoneinfo import ZoneInfo

@pytest.fixture(autouse=True)
def mock_yfinance(monkeypatch):
    def mock_download(tickers, start,end=None,interval=None,ignore_tz=False):
        is_hourly = interval and interval == '1h'
        datetime_delta = end-start
        if is_hourly:
            datetime_index = [
                datetime.combine(
                    start.date(),
                    time(hour=hour, minute=30),
                    tzinfo=ZoneInfo("America/New_York")
                ) + timedelta(days=day + 1) 
            for day in range(datetime_delta.days - 1) for hour in range(9, 16)]
        else:
            datetime_index = [start + timedelta(days=day + 1) for day in range(datetime_delta.days - 1)]
        dt_size = len(datetime_index)
        return pd.DataFrame(
            {
                'Open': [random.random() * 100 for _ in range(dt_size)],
                'High': [random.random() * 100 for _ in range(dt_size)],
                'Low': [random.random() * 100 for _ in range(dt_size)],
                'Close': [random.random() * 100 for _ in range(dt_size)],
                'Adj Close': [random.random() * 100 for _ in range(dt_size)],
                'Volume': [random.random() * 100 for _ in range(dt_size)],
            },
            index=pd.DatetimeIndex(datetime_index)
        )
    monkeypatch.setattr(
        yfinance,
        "download",
        mock_download
    )
