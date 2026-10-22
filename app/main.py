"""App entry point."""
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import cv, interview

app = FastAPI(title="AI Career Coach")

allowed_origins = ["http://localhost:5173"]
frontend_origin = os.getenv("FRONTEND_ORIGIN")
if frontend_origin:
    allowed_origins.append(frontend_origin.rstrip("/"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(cv.router)
app.include_router(interview.router)

@app.get("/api/health")
def health():
    return {"status": "ok"}
