from datetime import datetime, time

from sqlalchemy import TIMESTAMP, Column, Enum, String
from sqlalchemy.orm import relationship

from extractors.base import BaseExtractor
from models.base_model import BaseModel
from models.model_enums import PriceFrequency
from utils.enums import BaseEnum
from utils.string import camel_to_snake_case


class InstrumentType(BaseEnum):
    EQUITY = "EQUITY"
    INDICE = "INDICE"
    FOREX = "FOREX"
    COMMO = "COMMO"
    IRATE = "IRATE"


class CountryCode(BaseEnum):
    SWEDEN = "SWEDEN"
    US = "US"
    EMU = "EMU"


MARKET_TIMEFRAMES = {
    (InstrumentType.EQUITY, CountryCode.SWEDEN): [time(9, 30), time(15, 30)],
    (InstrumentType.EQUITY, CountryCode.US): [time(9, 30), time(15, 30)],
    (InstrumentType.EQUITY, CountryCode.EMU): [time(9), time(17)],
}


class DataExtractionClass(BaseEnum):
    YFINANCE = "YFinanceExtractor"


class Instrument(BaseModel):
    """
    Model representing a ticker
    """

    code = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, unique=True, index=True, nullable=False)
    yfinance_code = Column(String, unique=True, nullable=False)
    sector = Column(String, nullable=False)
    country_code = Column(Enum(CountryCode, native_enum=False), nullable=False)
    type = Column(Enum(InstrumentType, native_enum=False), nullable=False)
    earning_publication_date = Column(TIMESTAMP(), nullable=False)
    data_extraction_class = Column(Enum(DataExtractionClass, native_enum=False), nullable=False)

    timeseries = relationship("HourlyPriceTimeseries", cascade="all, delete")
    daily_features = relationship("DailyFeaturesTimeseries", cascade="all, delete")

    def get_extract_cls(self) -> BaseExtractor:
        try:
            # return self.data_extraction_class
            return getattr(
                __import__(
                    f"extractors.{camel_to_snake_case(self.data_extraction_class)}",
                    fromlist=[self.data_extraction_class],
                ),
                self.data_extraction_class,
            )
        except Exception as exc:
            print(type(exc))
