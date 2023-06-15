from .base_crud import BaseCrud
from models import TradingModel
from datetime import datetime
from sqlalchemy import select
from database import get_db
class TradingModelCrud(BaseCrud):
    base_cls = TradingModel

    @classmethod
    def get_instrument_timeseries(cls, model_id: str):
        '''
        Return per ticker all timeseries within the TradingModelInstrument defined interval
        '''
        # stmt = select(Instrument).where(
        #     Instrument.
        # )
        pass

    @classmethod
    def get_active_trading_models(cls)-> list[TradingModel]:
        '''
        Return all active trading models persisted in database
        '''
        db = next(get_db())
        stmt = select(TradingModel).filter_by(is_active=True)
        return db.execute(stmt).scalars().all()

