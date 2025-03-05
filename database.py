# Fixed incomplete variable, added error handling, and improved security

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from urllib.parse import quote_plus

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    db_user = os.environ.get("DB_USER", "postgres")
    db_password = os.environ.get("DB_PASSWORD", "")
    db_host = os.environ.get("DB_HOST", "localhost")
    db_name = os.environ.get("DB_NAME", "fastapi_db")
    DATABASE_URL = f"postgresql://{db_user}:{quote_plus(db_password)}@{db_host}/{db_name}"

try:
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
except Exception as e:
    print(f"Error connecting to the database: {e}")
    raise

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()