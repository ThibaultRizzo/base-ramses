"""
Module for dataset
"""

from datetime import datetime

import models

instruments = (
    {
        "id": "11111111-1111-1111-9111-111111111111",
        "code": "MSFT",
        "description": "Microsoft ticker",
        "yfinance_code": "MSFT",
        "sector": "tech",
        "country_code": models.instrument.CountryCode.US,
        "type": models.InstrumentType.EQUITY,
        "earning_publication_date": datetime.now(),
        "data_extraction_class": models.DataExtractionClass.YFINANCE,
    },
)

hourlyPriceTimeseries = (
    {
        "id": "11111111-1111-1111-9111-111111111111",
        "instrument_id": "11111111-1111-1111-9111-111111111111",
        "close": "1.700040536249836",
        "date": "2020-02-04 13:30:00",
        "frequency": "HOURLY",
        "high": "42.909724368286675",
        "low": "0.5165500845353721",
        "open": "95.20456096309188",
        "volume": "46.10415667379834",
    },
    {
        "id": "11111111-1111-1111-9111-111111111112",
        "instrument_id": "11111111-1111-1111-9111-111111111111",
        "close": "82.86499498153572",
        "date": "2020-02-04 14:30:00",
        "frequency": "HOURLY",
        "high": "63.84775960478427",
        "low": "8.361484779587991",
        "open": "55.8861475651443",
        "volume": "81.64236410369793",
    },
    {
        "id": "11111111-1111-1111-9111-111111111113",
        "instrument_id": "11111111-1111-1111-9111-111111111111",
        "close": "93.62927796358929",
        "date": "2020-02-04 15:30:00",
        "frequency": "HOURLY",
        "high": "89.83102543211035",
        "low": "9.031703632818077",
        "open": "14.72299162754397",
        "volume": "96.90013459251503",
    },
)

DATA_SET = {models.Instrument: instruments, models.HourlyPriceTimeseries: hourlyPriceTimeseries}
