# Fixed incomplete variable, added error handling, and improved type hints

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from typing import Optional

DATABASE_URL: str = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

engine = create_engine(DATABASE_URL)
SessionLocal: sessionmaker = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base: declarative_base = declarative_base()

def get_db() -> Optional[SessionLocal]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()