from sqlalchemy import Column, Float, String
from sqlalchemy.orm import relationship

from models.base_model import BaseModel


class Broker(BaseModel):
    """
    Model representing a broker
    """

    username = Column(String, unique=True, index=True, nullable=False)
    api_key = Column(String, unique=True, nullable=False)
    equity_fees = Column(Float(), nullable=False)
    equity_margin_req = Column(Float(), nullable=False)
    indice_fees = Column(Float(), nullable=False)
    indice_margin_req = Column(Float(), nullable=False)
    forex_fees = Column(Float(), nullable=False)
    forex_margin_req = Column(Float(), nullable=False)
    commodity_fees = Column(Float(), nullable=False)
    commodity_margin_req = Column(Float(), nullable=False)
    irate_fees = Column(Float(), nullable=False)
    irate_margin_req = Column(Float(), nullable=False)

    portfolio_lines = relationship("PortfolioLine")
