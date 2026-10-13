from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import uuid4
import json

from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Event, Attacker, Alert
from app.services.enrichment import enrich_ip
from app.services.telegram import send_telegram_alert

router = APIRouter(prefix="/webhook", tags=["webhook"])

class CloudTrailEvent(BaseModel):
    token_id: str
    event_name: str
    source_ip: str
    user_agent: Optional[str] = "unknown"
    event_time: Optional[str] = None
    aws_region: Optional[str] = "unknown"
    account_id: Optional[str] = "unknown"
    raw_event: Optional[Dict[str, Any]] = None

@router.post("/cloudtrail")
async def receive_cloudtrail_event(event: CloudTrailEvent, db: Session = Depends(get_db)):
    print(f"CANARY TRIGGERED: {event.token_id} from {event.source_ip}")
    
    enriched = await enrich_ip(event.source_ip)
    geo = enriched.get("geo", {})
    abuse = enriched.get("abuse", {})
    threat_level = enriched.get("threat_level", "unknown")
    abuse_score = enriched.get("abuse_score", 0)
    
    event_id = str(uuid4())
    
    db_event = Event(
        event_id=event_id, token_id=event.token_id, event_name=event.event_name,
        source_ip=event.source_ip, user_agent=event.user_agent,
        aws_region=event.aws_region, account_id=event.account_id,
        threat_level=threat_level, abuse_score=abuse_score,
        geo_data=json.dumps(geo), abuse_data=json.dumps(abuse),
        event_time=datetime.utcnow(), received_at=datetime.utcnow()
    )
    db.add(db_event)
    
    attacker = db.query(Attacker).filter(Attacker.ip == event.source_ip).first()
    if attacker:
        attacker.total_triggers += 1
        attacker.last_seen = datetime.utcnow()
    else:
        attacker = Attacker(
            ip=event.source_ip, country=geo.get("country"),
            city=geo.get("city"), org=geo.get("org"),
            abuse_score=abuse_score, total_triggers=1
        )
        db.add(attacker)
    
    # Send Telegram alert
    alert_payload = {
        "token_id": event.token_id, "event_name": event.event_name,
        "source_ip": event.source_ip,
        "event_time": event.event_time or datetime.utcnow().isoformat(),
        "threat_level": threat_level, "geo": geo, "abuse": abuse
    }
    telegram_result = await send_telegram_alert(alert_payload)
    print(f"Telegram: {telegram_result}")
    
    alert = Alert(
        event_id=event_id, channel="telegram",
        status=telegram_result.get("status", "unknown"),
        message=json.dumps(alert_payload)
    )
    db.add(alert)
    
    db.commit()
    print(f"Event stored: {event_id}")
    
    return {
        "status": "received", "event_id": event_id,
        "threat_level": threat_level,
        "telegram": telegram_result.get("status")
    }
