from __future__ import annotations

from datetime import datetime, timedelta
from typing import TYPE_CHECKING

import yfinance as yf

from database import get_db
from models import HourlyPriceTimeseries
from models.model_enums import PriceFrequency

from .base import BaseExtractor

if TYPE_CHECKING:
    from models import Instrument


class YFinanceExtractor(BaseExtractor):
    ticker_column = "yfinance_code"

    @classmethod
    def pull(
        cls,
        instrument: Instrument,
        end_date: datetime,
        start_date: datetime = None,
        frequency: PriceFrequency = PriceFrequency.DAILY,
    ):
        """"""
        start_date = start_date or end_date - timedelta(days=1)
        data = yf.download(
            tickers=[instrument.yfinance_code],
            start=start_date,
            end=end_date,
            interval=frequency.get_interval(),
            ignore_tz=False,
        )
        # data.index = data.index.map(lambda d: d.isoformat())
        return data.to_dict("index")

    # @classmethod
    # def pull_and_save(cls, instrument: Instrument, end_date: datetime, start_date: datetime = None):
    #     data_dict = cls.pull(instrument, end_date, start_date, PriceFrequency.HOURLY)
    #     db = next(get_db())
    #     timeseries = []
    #     for ts in data_dict:
    #         _dict = data_dict[ts]
    #         timeseries.append(
    #             HourlyPriceTimeseries(
    #                 date=ts,
    #                 open=_dict.get('Open'),
    #                 high=_dict.get('High'),
    #                 low=_dict.get('Low'),
    #                 close=_dict.get('Close'),
    #                 volume=_dict.get('Volume'),
    #                 frequency=PriceFrequency.HOURLY,
    #                 instrument_id=instrument.id,
    #             )
    #         )
    #     db.add_all(timeseries)
    #     db.commit()
