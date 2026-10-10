import asyncio
from app.services.ipinfo import get_ip_info
from app.services.abuseipdb import check_ip_abuse

async def enrich_ip(ip: str) -> dict:
    geo_task = get_ip_info(ip)
    abuse_task = check_ip_abuse(ip)
    
    geo_data, abuse_data = await asyncio.gather(geo_task, abuse_task)
    
    abuse_score = abuse_data.get("abuse_score", 0)
    if abuse_score >= 75:
        threat_level = "critical"
    elif abuse_score >= 50:
        threat_level = "high"
    elif abuse_score >= 25:
        threat_level = "medium"
    elif abuse_score > 0:
        threat_level = "low"
    else:
        threat_level = "unknown"
    
    return {
        "ip": ip,
        "geo": geo_data,
        "abuse": abuse_data,
        "threat_level": threat_level,
        "abuse_score": abuse_score
    }
