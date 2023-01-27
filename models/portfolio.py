from models.base_model import BaseModel
from sqlalchemy import Column, String, ForeignKey, Float, Integer
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID

class PortfolioLine(BaseModel):
    """
    Model representing a portfolio line
    """
    portfolio_id = Column(UUID(as_uuid=True), ForeignKey("portfolio.id"), nullable=False)
    instrument_id = Column(UUID(as_uuid=True), ForeignKey("instrument.id"), nullable=False)
    broker_id = Column(UUID(as_uuid=True), ForeignKey("broker.id"), nullable=False)
    quantity= Column(Integer(), nullable=False)


class Portfolio(BaseModel):
    """
    Model representing a portfolio
    """
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    net_asset_value= Column(Float(), nullable=False, default=0)

    user = relationship("User", viewonly=True)
