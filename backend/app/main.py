from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.routes import webhook, events

load_dotenv()

app = FastAPI(
    title="CloudCanary API",
    description="Decoy Cloud Credential Trap & Real-Time Breach Alert System",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(webhook.router)
app.include_router(events.router)

@app.get("/")
async def root():
    return {
        "name": "CloudCanary API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": [
            "POST /webhook/cloudtrail",
            "GET /events",
            "GET /events/stats",
            "GET /events/{event_id}",
            "GET /docs"
        ]
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}
