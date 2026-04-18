from sqlalchemy import Column, Integer, String, DateTime
from backend.core.database import Base
from datetime import datetime

class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    hcp_name = Column(String(255))
    interaction_date = Column(DateTime, default=datetime.utcnow)
    attendees = Column(String(255))
    topics = Column(String(500))
    sentiment = Column(String(50))
    outcomes = Column(String(500))