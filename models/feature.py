from models.base_model import BaseModel
from sqlalchemy import Column, String

class Feature(BaseModel):
    code = Column(String, unique=True, index=True, nullable=False)
    function_name: str
    feature_list: List[Feature]
    instrument_list: List[Instrument]



