# backend/schemas.py
from pydantic import BaseModel

class MailIn(BaseModel):
    sender: str
    receiver: str | None = None
    subject: str | None = ""
    body: str

class MailOut(BaseModel):
    id: int
    sender: str
    receiver: str | None
    subject: str | None
    body: str
    prediction: str

    class Config:
        orm_mode = True
