from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from contextlib import asynccontextmanager

from app.routes import webhook, events
from app.database import init_db

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title="CloudCanary API",
    description="Decoy Cloud Credential Trap & Real-Time Breach Alert System",
    version="1.0.0",
    lifespan=lifespan
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
        "database": "postgresql (supabase)"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}
