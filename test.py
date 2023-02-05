# import yfinance as yf
# data = yf.download("MSFT", start="2023-01-02", end="2023-01-06", interval = "1h", ignore_tz = False)
# # data.index = data.index.map(lambda d: d.isoformat())
# print(f"data {data}")
# print('_______')
# data = yf.download("TTE.PA", start="2023-01-02", end="2023-01-06", interval = "1h", ignore_tz = False)
# # data.index = data.index.map(lambda d: d.isoformat())
# print(f"data {data}")

from crud.instrument_crud import InstrumentCrud
from database import get_db
import models
from datetime import datetime

session = next(get_db())
# instrument_id = "11111111-1111-1111-9111-111111111111"
# instrument = InstrumentCrud.get_by_id(session, instrument_id)
# instrument = InstrumentCrud.create_one(session, {
#     "code":"AAPL",
#     "description" : "Apple ticker",
#     "yfinance_code" :"AAPL",
#     "sector" :"tech",
#     "country_code" :models.instrument.CountryCode.US,
#     "type" :models.InstrumentType.EQUITY,
#     "earning_publication_date" :datetime.now(),
#     "data_extraction_class" :models.DataExtractionClass.YFINANCE
# })
# session.commit()
timeries = InstrumentCrud.get_timeseries(session, 'AAPL', datetime(2023, 1, 10), datetime(2023, 1, 15))
print(f"timeseries {timeries}")
session.commit()
