"""
OpsPilot AI

Main FastAPI application.
"""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.core.config import settings
from backend.core.database import create_tables

# Routers
from backend.routers.auth import router as auth_router


# ==========================================================
# Lifespan
# ==========================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup and shutdown events.
    """

    # Development only
    if settings.DEBUG:
        create_tables()

    yield


# ==========================================================
# FastAPI App
# ==========================================================

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
    lifespan=lifespan,
)

# ==========================================================
# CORS
# ==========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================================
# Routes
# ==========================================================

@app.get("/", tags=["Root"])
def root():
    """
    Root endpoint.
    """
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "status": "running",
    }


@app.get("/health", tags=["Health"])
def health():
    """
    Health check endpoint.
    """
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
    }


# ==========================================================
# API Routers
# ==========================================================

app.include_router(
    auth_router,
    prefix=settings.API_PREFIX,
)