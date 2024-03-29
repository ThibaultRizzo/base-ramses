from datetime import datetime

from sqlalchemy import select

from models import TradingModel

from .base_crud import BaseCrud


class TradingModelCrud(BaseCrud):
    base_cls = TradingModel

    @classmethod
    def get_instrument_timeseries(cls, model_id: str):
        """
        Return per ticker all timeseries within the TradingModelInstrument defined interval
        """
        pass
        # stmt = select(Instrument).where(
        #     Instrument.
        # )
