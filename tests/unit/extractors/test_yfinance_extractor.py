from datetime import datetime

from sqlalchemy import select

from crud.instrument_crud import InstrumentCrud
from database import get_db
from models import DataExtractionClass, Instrument, InstrumentType
from models.model_enums import PriceFrequency
from utils.testing import compare_item, compare_list


def test_pull_and_save_yfinance_extraction(db):
    instrument_id = "11111111-1111-1111-9111-111111111111"
    timeseries = InstrumentCrud.pull(
        db, instrument_id, datetime(2020, 2, 5), datetime(2020, 2, 2), PriceFrequency.HOURLY
    )
    assert len(timeseries) == 21
