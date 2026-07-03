# backend/database.py
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker, declarative_base
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "data" / "inbox.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Mail(Base):
    __tablename__ = "inbox"
    id = Column(Integer, primary_key=True, index=True)
    sender = Column(String(200))
    receiver = Column(String(200))
    subject = Column(String(500))
    body = Column(Text)
    prediction = Column(String(50), default="Not Scanned")

def init_db():
    Base.metadata.create_all(bind=engine)
