import os
import httpx

ABUSEIPDB_KEY = os.getenv("ABUSEIPDB_KEY", "")
ABUSEIPDB_URL = "https://api.abuseipdb.com/api/v2/check"

async def check_ip_abuse(ip: str) -> dict:
    if not ABUSEIPDB_KEY:
        return {"error": "ABUSEIPDB_KEY not set"}
    
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(
                ABUSEIPDB_URL,
                params={"ipAddress": ip, "maxAgeInDays": 90},
                headers={
                    "Key": ABUSEIPDB_KEY,
                    "Accept": "application/json"
                }
            )
            response.raise_for_status()
            data = response.json().get("data", {})
            
            return {
                "ip": data.get("ipAddress"),
                "abuse_score": data.get("abuseConfidenceScore", 0),
                "total_reports": data.get("totalReports", 0),
                "country": data.get("countryCode"),
                "isp": data.get("isp"),
                "domain": data.get("domain"),
                "is_public": data.get("isPublic"),
                "is_whitelisted": data.get("isWhitelisted"),
                "last_reported": data.get("lastReportedAt")
            }
    except Exception as e:
        return {"error": str(e)}
