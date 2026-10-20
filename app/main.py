"""App entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import cv

app = FastAPI(title="AI Career Coach")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://ai-career-coach-blue-nine.vercel.app"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cv.router)

@app.get("/api/health")
def health():
    return {"status": "ok"}
