from sqlalchemy import TIMESTAMP, Column, Date, Enum, Float, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models.base_model import BaseModel
from models.model_enums import PriceFrequency


class HourlyPriceTimeseries(BaseModel):
    """
    Hourly timeseries
    """

    date = Column(TIMESTAMP(timezone=True), nullable=False)
    open = Column(Float(), nullable=False)
    high = Column(Float(), nullable=False)
    low = Column(Float(), nullable=False)
    close = Column(Float(), nullable=False)
    volume = Column(Float(), nullable=False)
    frequency = Column(Enum(PriceFrequency, native_enum=False), nullable=False)

    instrument_id = Column(UUID(as_uuid=True), ForeignKey("instrument.id"), nullable=False)
    instrument = relationship("Instrument", viewonly=True)

    __table_args__ = (
        Index(
            "unique_ticker_date",
            date,
            instrument_id,
            unique=True,
        ),
    )


class DailyFeaturesTimeseries(BaseModel):
    """
    Daily features timeseries
    """

    date = Column(Date(), nullable=False)
    sector_pe = Column(Float(), nullable=False)
    pe = Column(Float(), nullable=False)
    instrument_id = Column(UUID(as_uuid=True), ForeignKey("instrument.id", ondelete="CASCADE"), nullable=False)
    instrument = relationship("Instrument", viewonly=True)
