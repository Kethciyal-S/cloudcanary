import os
import httpx

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"


async def send_telegram_alert(event: dict) -> dict:
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return {"status": "failed", "error": "Telegram credentials not set"}
    
    token_id = event.get("token_id", "unknown")
    source_ip = event.get("source_ip", "unknown")
    event_name = event.get("event_name", "unknown")
    threat_level = event.get("threat_level", "unknown")
    geo = event.get("geo", {})
    abuse = event.get("abuse", {})
    event_time = event.get("event_time", "unknown")
    
    country = geo.get("country", "N/A")
    city = geo.get("city", "N/A")
    org = geo.get("org", "N/A")
    abuse_score = abuse.get("abuse_score", 0)
    
    message = f"""CANARY TRIGGERED

Token: {token_id}
Event: {event_name}
Time: {event_time}

Attacker Info:
* IP: {source_ip}
* Country: {country}
* City: {city}
* ISP/Org: {org}
* Abuse Score: {abuse_score}/100

Threat Level: {threat_level.upper()}

CloudCanary Alert System"""
    
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(
                TELEGRAM_API_URL,
                json={
                    "chat_id": TELEGRAM_CHAT_ID,
                    "text": message,
                }
            )
            response.raise_for_status()
            return {"status": "sent"}
    except Exception as e:
        return {"status": "failed", "error": str(e)}
