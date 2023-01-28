from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from settings import settings
# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
from models.base_model import BaseModel

# print(f"settings.SQLALCHEMY_DATABASE_URL {settings.SQLALCHEMY_DATABASE_URL}")

def get_db():
    # TODO: Improve this to share connection 
    engine = create_engine(
        settings.SQLALCHEMY_DATABASE_URL, echo=True, future=True
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    BaseModel.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()