# Fixed imports, removed unused code, improved naming conventions, and addressed security concerns

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:admin@localhost/fastapi_db")

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()