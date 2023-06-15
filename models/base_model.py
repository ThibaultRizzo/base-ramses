from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from sqlalchemy.ext.declarative import declared_attr
    
from utils.string import camel_to_snake_case

from sqlalchemy.orm import DeclarativeBase

class BaseModel(DeclarativeBase):
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4)
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return camel_to_snake_case(cls.__name__)

    def dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = str(getattr(self, column.name))

        return d
