from datetime import datetime

from crud.instrument_crud import InstrumentCrud
from utils.testing import compare_item, compare_list


def test_get_timeseries(db):
    instrument_code = "MSFT"
    compare_list(
        [
            {
                "date": "2022-02-05 20:30:00+00:00",
                "frequency": "HOURLY",
                "instrument_id": "11111111-1111-1111-9111-111111111111",
            },
            {
                "date": "2022-02-05 19:30:00+00:00",
                "frequency": "HOURLY",
                "instrument_id": "11111111-1111-1111-9111-111111111111",
            },
            {
                "date": "2022-02-05 18:30:00+00:00",
                "frequency": "HOURLY",
                "instrument_id": "11111111-1111-1111-9111-111111111111",
            },
            {
                "date": "2022-02-05 17:30:00+00:00",
                "frequency": "HOURLY",
                "instrument_id": "11111111-1111-1111-9111-111111111111",
            },
            {
                "date": "2022-02-05 16:30:00+00:00",
                "frequency": "HOURLY",
                "instrument_id": "11111111-1111-1111-9111-111111111111",
            },
            {
                "date": "2022-02-05 15:30:00+00:00",
                "frequency": "HOURLY",
                "instrument_id": "11111111-1111-1111-9111-111111111111",
            },
            {
                "date": "2022-02-05 14:30:00+00:00",
                "frequency": "HOURLY",
                "instrument_id": "11111111-1111-1111-9111-111111111111",
            },
            {
                "date": "2022-02-04 20:30:00+00:00",
                "frequency": "HOURLY",
                "instrument_id": "11111111-1111-1111-9111-111111111111",
            },
            {
                "date": "2022-02-04 19:30:00+00:00",
                "frequency": "HOURLY",
                "instrument_id": "11111111-1111-1111-9111-111111111111",
            },
            {
                "date": "2022-02-04 18:30:00+00:00",
                "frequency": "HOURLY",
                "instrument_id": "11111111-1111-1111-9111-111111111111",
            },
            {
                "date": "2022-02-04 17:30:00+00:00",
                "frequency": "HOURLY",
                "instrument_id": "11111111-1111-1111-9111-111111111111",
            },
            {
                "date": "2022-02-04 16:30:00+00:00",
                "frequency": "HOURLY",
                "instrument_id": "11111111-1111-1111-9111-111111111111",
            },
            {
                "date": "2022-02-04 15:30:00+00:00",
                "frequency": "HOURLY",
                "instrument_id": "11111111-1111-1111-9111-111111111111",
            },
            {
                "date": "2022-02-04 14:30:00+00:00",
                "frequency": "HOURLY",
                "instrument_id": "11111111-1111-1111-9111-111111111111",
            },
            {
                "date": "2022-02-03 20:30:00+00:00",
                "frequency": "HOURLY",
                "instrument_id": "11111111-1111-1111-9111-111111111111",
            },
            {
                "date": "2022-02-03 19:30:00+00:00",
                "frequency": "HOURLY",
                "instrument_id": "11111111-1111-1111-9111-111111111111",
            },
            {
                "date": "2022-02-03 18:30:00+00:00",
                "frequency": "HOURLY",
                "instrument_id": "11111111-1111-1111-9111-111111111111",
            },
            {
                "date": "2022-02-03 17:30:00+00:00",
                "frequency": "HOURLY",
                "instrument_id": "11111111-1111-1111-9111-111111111111",
            },
            {
                "date": "2022-02-03 16:30:00+00:00",
                "frequency": "HOURLY",
                "instrument_id": "11111111-1111-1111-9111-111111111111",
            },
            {
                "date": "2022-02-03 15:30:00+00:00",
                "frequency": "HOURLY",
                "instrument_id": "11111111-1111-1111-9111-111111111111",
            },
            {
                "date": "2022-02-03 14:30:00+00:00",
                "frequency": "HOURLY",
                "instrument_id": "11111111-1111-1111-9111-111111111111",
            },
            {
                "date": "2022-02-02 20:30:00+00:00",
                "frequency": "HOURLY",
                "instrument_id": "11111111-1111-1111-9111-111111111111",
            },
            {
                "date": "2022-02-02 19:30:00+00:00",
                "frequency": "HOURLY",
                "instrument_id": "11111111-1111-1111-9111-111111111111",
            },
            {
                "date": "2022-02-02 18:30:00+00:00",
                "frequency": "HOURLY",
                "instrument_id": "11111111-1111-1111-9111-111111111111",
            },
            {
                "date": "2022-02-02 17:30:00+00:00",
                "frequency": "HOURLY",
                "instrument_id": "11111111-1111-1111-9111-111111111111",
            },
            {
                "date": "2022-02-02 16:30:00+00:00",
                "frequency": "HOURLY",
                "instrument_id": "11111111-1111-1111-9111-111111111111",
            },
            {
                "date": "2022-02-02 15:30:00+00:00",
                "frequency": "HOURLY",
                "instrument_id": "11111111-1111-1111-9111-111111111111",
            },
            {
                "date": "2022-02-02 14:30:00+00:00",
                "frequency": "HOURLY",
                "instrument_id": "11111111-1111-1111-9111-111111111111",
            },
        ],
        InstrumentCrud.get_timeseries(
            session=db, code=instrument_code, start_date=datetime(2022, 2, 2), end_date=datetime(2022, 2, 5)
        ),
    )
