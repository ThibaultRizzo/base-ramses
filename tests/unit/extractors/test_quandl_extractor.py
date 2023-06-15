from models import Instrument, InstrumentType, DataExtractionClass
from datetime import datetime
from utils.testing import compare_item, compare_list
from database import get_db
from sqlalchemy import select
from crud.instrument_crud import InstrumentCrud
from models.model_enums import PriceFrequency

def test_pull_and_save_yfinance_extraction(db):
    instrument_id = "11111111-1111-1111-9111-111111111111"
    timeseries = InstrumentCrud.pull(db, instrument_id, datetime(2020, 2,5), datetime(2020, 2,2), PriceFrequency.HOURLY)
    assert len(timeseries) == 21