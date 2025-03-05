# Fixed imports, removed incomplete line, renamed SessionLocal, added connection test

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:password@localhost/fastapi_db")

engine = create_engine(DATABASE_URL)
session_local = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

try:
    engine.connect()
    print("Database connection successful")
except Exception as e:
    print(f"Database connection failed: {str(e)}")