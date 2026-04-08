from sqlalchemy import Column, Integer, String, Float, Text
from .database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(255), nullable=False)
    total = Column(Float, nullable=False)
    status = Column(String(50), default="CREATED")
    items_json = Column(Text, nullable=False)
