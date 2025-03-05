# Updated database connection setup with improved security, error handling, and type hints

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
import os

DATABASE_URL: str = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

try:
    engine = create_engine(DATABASE_URL, pool_size=5, max_overflow=10)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
except SQLAlchemyError as e:
    raise Exception(f"Failed to connect to the database: {str(e)}")

def get_db() -> Optional[SessionLocal]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()