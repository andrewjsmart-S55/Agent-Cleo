"""
Agent-Cleo v2.1 - High Performance FastAPI Application
Refactored for deployment on theoverlord.ai
"""
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from loguru import logger
import sys

from .config import settings
from .database import init_db
from .api import api_router, health_router

# Configure loguru
logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO"
)
logger.add(
    "logs/agent_cleo.log",
    rotation="10 MB",
    retention="7 days",
    level="DEBUG"
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown"""
    # Startup
    logger.info("=" * 70)
    logger.info("Agent-Cleo v2.1 - High Performance AI Agent Orchestration")
    logger.info("=" * 70)

    logger.info("Initializing database...")
    init_db()
    logger.info(f"Database initialized: {settings.database_url}")
    logger.info(f"Overlord API: {settings.overlord_api_url}")

    # No filesystem agent discovery in production
    # Agents are managed via database for better performance
    logger.info("Agent management via database (no filesystem scanning)")

    logger.info("=" * 70)
    logger.info("Application ready to accept requests")
    logger.info("=" * 70)

    yield

    # Shutdown
    logger.info("Shutting down Agent-Cleo...")


# Initialize FastAPI app
app = FastAPI(
    title="Agent-Cleo",
    version="2.1.0",
    description="High Performance AI Agent Orchestration for theoverlord.ai",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware with performance settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
    max_age=3600,  # Cache preflight requests for 1 hour
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Include API routers
app.include_router(api_router)
app.include_router(health_router)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the main application interface"""
    return templates.TemplateResponse("index_new.html", {"request": request})


@app.get("/status")
async def status():
    """Quick status check (lighter than /health)"""
    return {"status": "ok", "version": settings.app_version}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.app:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        workers=1,  # Single worker for now, can scale with Redis-backed state
        access_log=True
    )
