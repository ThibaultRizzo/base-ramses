from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings

print(f"settings.get_database_uri()   {settings.get_database_uri()}")
engine = create_engine(settings.get_database_uri(), pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
def get_session():
    