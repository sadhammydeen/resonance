"""
Resonance Without Sound - Backend API
Main FastAPI application entry point
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from pathlib import Path
import shutil
from typing import Dict, Any

from api.routes import analysis_router
from services.config import settings

# Create FastAPI app
app = FastAPI(
    title="Resonance Without Sound API",
    description="AI-powered music interpretation engine for learning without sound",
    version="0.1.0"
)

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(analysis_router, prefix="/api", tags=["analysis"])

# Create uploads directory
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Resonance Without Sound API",
        "version": "0.1.0"
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "components": {
            "api": "operational",
            "audio_processor": "ready",
            "llm_service": "ready" if settings.OPENAI_API_KEY else "not_configured"
        }
    }


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    print("🎵 Starting Resonance Without Sound API...")
    print(f"📁 Upload directory: {UPLOAD_DIR.absolute()}")
    print(f"🤖 LLM configured: {bool(settings.OPENAI_API_KEY)}")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("👋 Shutting down Resonance Without Sound API...")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
