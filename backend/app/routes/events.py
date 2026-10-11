from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, distinct
from datetime import datetime
import json

from app.database import get_db
from app.models import Event

router = APIRouter(prefix="/events", tags=["events"])

@router.get("")
async def list_events(limit: int = 50, db: Session = Depends(get_db)):
    events = db.query(Event).order_by(Event.received_at.desc()).limit(limit).all()
    result = []
    for e in events:
        result.append({
            "id": e.event_id,
            "token_id": e.token_id,
            "event_name": e.event_name,
            "source_ip": e.source_ip,
            "user_agent": e.user_agent,
            "aws_region": e.aws_region,
            "account_id": e.account_id,
            "threat_level": e.threat_level,
            "abuse_score": e.abuse_score,
            "geo": json.loads(e.geo_data) if e.geo_data else {},
            "abuse": json.loads(e.abuse_data) if e.abuse_data else {},
            "event_time": e.event_time.isoformat() if e.event_time else None,
            "received_at": e.received_at.isoformat() if e.received_at else None
        })
    total = db.query(Event).count()
    return {"total": total, "events": result}

@router.get("/stats")
async def get_stats(db: Session = Depends(get_db)):
    total = db.query(Event).count()
    critical = db.query(Event).filter(Event.threat_level == "critical").count()
    high = db.query(Event).filter(Event.threat_level == "high").count()
    unique_ips = db.query(func.count(distinct(Event.source_ip))).scalar()
    return {
        "total_triggers": total,
        "critical_threats": critical,
        "high_threats": high,
        "unique_attackers": unique_ips or 0,
        "last_updated": datetime.utcnow().isoformat()
    }

@router.get("/{event_id}")
async def get_event(event_id: str, db: Session = Depends(get_db)):
    e = db.query(Event).filter(Event.event_id == event_id).first()
    if not e:
        return {"error": "Event not found"}
    return {
        "id": e.event_id,
        "token_id": e.token_id,
        "event_name": e.event_name,
        "source_ip": e.source_ip,
        "threat_level": e.threat_level,
        "geo": json.loads(e.geo_data) if e.geo_data else {},
        "abuse": json.loads(e.abuse_data) if e.abuse_data else {},
        "received_at": e.received_at.isoformat() if e.received_at else None
    }
