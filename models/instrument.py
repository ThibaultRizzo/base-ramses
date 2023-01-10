from models.base_model import BaseModel
from sqlalchemy import Column, String, Enum, TIMESTAMP
from utils.enums import BaseEnum
from sqlalchemy.orm import relationship

class InstrumentType(BaseEnum):
    EQUITY = "EQUITY"
    INDICE = "INDICE"
    FOREX = "FOREX"
    COMMO = "COMMO"
    IRATE = "IRATE"

class Instrument(BaseModel):
    """
    Model representing a ticker
    """
    code = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, unique=True, index=True, nullable=False)
    yfinance_code = Column(String, unique=True, nullable=False)
    sector = Column(String, nullable=False)
    country_code = Column(String, nullable=False)
    type = Column(Enum(InstrumentType, native_enum=False), nullable=False)
    earning_publication_date = Column(TIMESTAMP(), nullable=False)

    timeseries = relationship("HourlyPriceTimeseries", cascade="all, delete")
    daily_features = relationship("DailyFeaturesTimeseries", cascade="all, delete")