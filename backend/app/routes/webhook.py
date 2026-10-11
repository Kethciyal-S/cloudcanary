from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import uuid4
import json

from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Event, Attacker
from app.services.enrichment import enrich_ip

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
        event_id=event_id,
        token_id=event.token_id,
        event_name=event.event_name,
        source_ip=event.source_ip,
        user_agent=event.user_agent,
        aws_region=event.aws_region,
        account_id=event.account_id,
        threat_level=threat_level,
        abuse_score=abuse_score,
        geo_data=json.dumps(geo),
        abuse_data=json.dumps(abuse),
        event_time=datetime.utcnow(),
        received_at=datetime.utcnow()
    )
    db.add(db_event)
    
    attacker = db.query(Attacker).filter(Attacker.ip == event.source_ip).first()
    if attacker:
        attacker.total_triggers += 1
        attacker.last_seen = datetime.utcnow()
    else:
        attacker = Attacker(
            ip=event.source_ip,
            country=geo.get("country"),
            city=geo.get("city"),
            org=geo.get("org"),
            abuse_score=abuse_score,
            total_triggers=1
        )
        db.add(attacker)
    
    db.commit()
    print(f"Event stored in DB: {event_id}")
    
    return {"status": "received", "event_id": event_id, "threat_level": threat_level}
