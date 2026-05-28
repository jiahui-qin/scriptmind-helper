"""FastAPI application entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import upload, analysis, tts, config
from app.database import create_tables

# Create FastAPI application instance
app = FastAPI(
    title="ScriptMind AI API",
    description="台本分析助手 - Script Analysis Assistant API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers with prefixes
app.include_router(upload.router, prefix="/api/v1/upload", tags=["upload"])
app.include_router(analysis.router, prefix="/api/v1/analysis", tags=["analysis"])
app.include_router(tts.router, prefix="/api/v1/tts", tags=["tts"])
app.include_router(config.router, prefix="/api/v1/config", tags=["config"])


@app.on_event("startup")
async def startup_event():
    """Initialize application on startup."""
    create_tables()


@app.get("/", tags=["root"])
async def root():
    """API root endpoint with basic information."""
    return {
        "name": "ScriptMind AI API",
        "version": "1.0.0",
        "description": "台本分析助手 - Script Analysis Assistant",
        "docs": "/docs",
        "status": "running"
    }


@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "ok",
        "service": "scriptmind-ai",
        "version": "1.0.0"
    }
