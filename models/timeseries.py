from models.base_model import BaseModel
from sqlalchemy import Column, ForeignKey, TIMESTAMP, Float, Date, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from utils.enums import BaseEnum

class PriceFrequency(BaseEnum):
    HOURLY = "HOURLY"
    DAILY = "DAILY"

class HourlyPriceTimeseries(BaseModel):
    """
    Hourly timeseries
    """
    date = Column(TIMESTAMP(), nullable=False)
    open= Column(Float(), nullable=False)
    high= Column(Float(), nullable=False)
    low= Column(Float(), nullable=False)
    close= Column(Float(), nullable=False)
    volume= Column(Float(), nullable=False)
    frequency = Column(Enum(PriceFrequency, native_enum=False), nullable=False)

    instrument_id = Column(UUID(as_uuid=True), ForeignKey("instrument.id", ondelete="CASCADE"), nullable=False)
    instrument = relationship("Instrument", backref="timeseries", passive_deletes=True)

class DailyFeaturesTimeseries(BaseModel):
    """
    Daily features timeseries
    """
    date = Column(Date(), nullable=False)
    sector_pe= Column(Float(), nullable=False)
    pe= Column(Float(), nullable=False)
    instrument_id = Column(UUID(as_uuid=True), ForeignKey("instrument.id", ondelete="CASCADE"), nullable=False)
    instrument = relationship("Instrument", backref="timeseries", passive_deletes=True)

