import json
import os
import urllib.request
from datetime import datetime

def lambda_handler(event, context):
    print("=" * 60)
    print("CANARY TRIGGERED!")
    print("=" * 60)
    print(json.dumps(event, indent=2))
    
    try:
        detail = event.get("detail", {})
        user_identity = detail.get("userIdentity", {})
        source_ip = detail.get("sourceIPAddress", "unknown")
        user_agent = detail.get("userAgent", "unknown")
        event_name = detail.get("eventName", "unknown")
        event_time = detail.get("eventTime", datetime.utcnow().isoformat())
        aws_region = detail.get("awsRegion", "unknown")
        user_name = user_identity.get("userName", "unknown")
        account_id = user_identity.get("accountId", "unknown")
        
        payload = {
            "token_id": user_name,
            "event_name": event_name,
            "source_ip": source_ip,
            "user_agent": user_agent,
            "event_time": event_time,
            "aws_region": aws_region,
            "account_id": account_id,
            "raw_event": detail
        }
        
        print("Payload to backend:")
        print(json.dumps(payload, indent=2))
        
        backend_url = os.environ.get("BACKEND_URL", "")
        
        if backend_url:
            req = urllib.request.Request(
                backend_url + "/webhook/cloudtrail",
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            try:
                with urllib.request.urlopen(req, timeout=10) as response:
                    print(f"Backend response: {response.status}")
            except Exception as e:
                print(f"Backend POST failed: {e}")
        else:
            print("BACKEND_URL not set — Part 4 la set pannuvom")
        
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Canary triggered", "token_id": user_name})
        }
    
    except Exception as e:
        print(f"Error: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
