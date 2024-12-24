from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import logging

from .api.v1.api import api_router
from .db.session import get_db
from .db.init_node_types import register_node_types

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Mati Workflow Engine",
    description="API for managing and executing AI workflows",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    logger.info("Initializing application...")
    
    # Register node types
    db = next(get_db())
    try:
        register_node_types(db)
        logger.info("Node types registered successfully")
    except Exception as e:
        logger.error(f"Error registering node types: {e}")
    finally:
        db.close()

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.get("/")
def root():
    """Root endpoint"""
    return {
        "name": "Mati Workflow Engine",
        "version": "1.0.0",
        "docs_url": "/docs",
        "openapi_url": "/openapi.json"
    }

# Error handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.exception("Unhandled exception")
    return {
        "detail": "Internal server error",
        "message": str(exc)
    }, 500
