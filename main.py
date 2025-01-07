from fastapi import FastAPI
from database import engine
from models import Base
from routes import router

app = FastAPI()

# Initialize database tables
Base.metadata.create_all(bind=engine)

# Include routes
app.include_router(router)
