from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class Token(Base):
    __tablename__ = "tokens"
    id = Column(Integer, primary_key=True, index=True)
    token_id = Column(String, unique=True, index=True, nullable=False)
    type = Column(String, default="aws_access_key")
    planted_location = Column(String)
    aws_user = Column(String)
    access_key_id = Column(String)
    secret_access_key = Column(String)
    status = Column(String, default="active")
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(String, unique=True, index=True)
    token_id = Column(String, index=True)
    event_name = Column(String)
    source_ip = Column(String, index=True)
    user_agent = Column(String)
    aws_region = Column(String)
    account_id = Column(String)
    threat_level = Column(String, default="unknown")
    abuse_score = Column(Integer, default=0)
    geo_data = Column(Text)
    abuse_data = Column(Text)
    event_time = Column(DateTime)
    received_at = Column(DateTime, default=datetime.utcnow)

class Attacker(Base):
    __tablename__ = "attackers"
    id = Column(Integer, primary_key=True, index=True)
    ip = Column(String, unique=True, index=True)
    country = Column(String)
    city = Column(String)
    org = Column(String)
    abuse_score = Column(Integer, default=0)
    total_triggers = Column(Integer, default=1)
    first_seen = Column(DateTime, default=datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.utcnow)

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(String, index=True)
    channel = Column(String)
    status = Column(String)
    message = Column(Text)
    sent_at = Column(DateTime, default=datetime.utcnow)
