from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import uuid4
from app.services.enrichment import enrich_ip
from app.routes.events import events_store

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
async def receive_cloudtrail_event(event: CloudTrailEvent):
    print(f"CANARY TRIGGERED: {event.token_id} from {event.source_ip}")
    
    enriched = await enrich_ip(event.source_ip)
    
    payload = {
        "id": str(uuid4()),
        "token_id": event.token_id,
        "event_name": event.event_name,
        "source_ip": event.source_ip,
        "user_agent": event.user_agent,
        "event_time": event.event_time or datetime.utcnow().isoformat(),
        "aws_region": event.aws_region,
        "account_id": event.account_id,
        "geo": enriched.get("geo", {}),
        "abuse": enriched.get("abuse", {}),
        "threat_level": enriched.get("threat_level", "unknown"),
        "abuse_score": enriched.get("abuse_score", 0),
        "received_at": datetime.utcnow().isoformat()
    }
    
    events_store.append(payload)
    print(f"Event stored. Total: {len(events_store)}")
    
    return {
        "status": "received",
        "event_id": payload["id"],
        "threat_level": payload["threat_level"]
    }
