from models.base_model import BaseModel
from sqlalchemy import Column, String, TIMESTAMP
from sqlalchemy.orm import relationship
from datetime import datetime

class User(BaseModel):
    """
    Model representing a user
    """
    username = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String, unique=True, nullable=False)
    last_name = Column(String, unique=True, nullable=False)

    created_at = Column(TIMESTAMP(), nullable=False, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP(), nullable=False, onupdate=datetime.utcnow, default=datetime.utcnow)

    portfolios = relationship("Portfolio", cascade="all, delete")