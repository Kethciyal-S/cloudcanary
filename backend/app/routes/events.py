from fastapi import APIRouter
from datetime import datetime

router = APIRouter(prefix="/events", tags=["events"])
events_store = []

@router.get("")
async def list_events(limit: int = 50):
    return {"total": len(events_store), "events": events_store[-limit:]}

@router.get("/stats")
async def get_stats():
    total = len(events_store)
    critical = sum(1 for e in events_store if e.get("threat_level") == "critical")
    high = sum(1 for e in events_store if e.get("threat_level") == "high")
    unique_ips = len(set(e.get("source_ip") for e in events_store))
    
    return {
        "total_triggers": total,
        "critical_threats": critical,
        "high_threats": high,
        "unique_attackers": unique_ips,
        "last_updated": datetime.utcnow().isoformat()
    }

@router.get("/{event_id}")
async def get_event(event_id: str):
    for event in events_store:
        if event.get("id") == event_id:
            return event
    return {"error": "Event not found"}
