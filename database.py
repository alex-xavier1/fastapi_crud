# Fixed syntax error, improved security, added error handling and connection test

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
import logging

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    logging.warning("DATABASE_URL not set. Using default local database.")
    DATABASE_URL = "postgresql://postgres:admin@localhost/fastapi_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

try:
    with engine.connect() as connection:
        connection.execute("SELECT 1")
    logging.info("Database connection successful")
except Exception as e:
    logging.error(f"Database connection failed: {e}")