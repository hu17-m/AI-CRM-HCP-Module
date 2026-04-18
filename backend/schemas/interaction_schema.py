from pydantic import BaseModel
from datetime import datetime


class InteractionCreate(BaseModel):
    hcp_name: str
    interaction_date: datetime
    topics: str
    sentiment: str
    outcomes: str


class InteractionResponse(InteractionCreate):
    id: int

    class Config:
        from_attributes = True