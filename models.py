#changes done...models updated...updatedlist
from sqlalchemy import Column, Integer, String
from database import Base
import datetime
import json

class Item(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Integer)
    quantity = Column(Integer)
