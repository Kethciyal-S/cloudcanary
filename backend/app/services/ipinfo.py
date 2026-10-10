import os
import httpx

IPINFO_TOKEN = os.getenv("IPINFO_TOKEN", "")
IPINFO_URL = "https://ipinfo.io/{ip}/json"

async def get_ip_info(ip: str) -> dict:
    if not IPINFO_TOKEN:
        return {"error": "IPINFO_TOKEN not set"}
    
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(
                IPINFO_URL.format(ip=ip),
                params={"token": IPINFO_TOKEN}
            )
            response.raise_for_status()
            data = response.json()
            
            return {
                "ip": data.get("ip"),
                "city": data.get("city"),
                "region": data.get("region"),
                "country": data.get("country"),
                "loc": data.get("loc"),
                "org": data.get("org"),
                "timezone": data.get("timezone")
            }
    except Exception as e:
        return {"error": str(e)}
