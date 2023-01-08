from models.base_model import BaseModel
from sqlalchemy import Column, ForeignKey, TIMESTAMP, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

class RawDataTimeseries(BaseModel):
    """
    Timeseries linked to a givne isntrument
    """
    date = Column(TIMESTAMP(), nullable=False)
    open= Column(Float(), nullable=False)
    high= Column(Float(), nullable=False)
    low= Column(Float(), nullable=False)
    close= Column(Float(), nullable=False)
    instrument_id = Column(UUID(as_uuid=True), ForeignKey("instrument.id", ondelete="CASCADE"), nullable=False)
    instrument = relationship("Instrument", backref="timeseries", passive_deletes=True)
