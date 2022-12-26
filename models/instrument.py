from .base_model import BaseModel
from sqlalchemy import Column, Enum, String

class Instrument(BaseModel):
    code = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, unique=True, index=True, nullable=False)
    yfinance_code = Column(String, unique=True, nullable=False)
    # reuters_code = Column(String, unique=True, nullable=False)