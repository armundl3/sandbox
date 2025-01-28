from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as api_router
from app.core.config import settings
from app.core.model_loader import ModelLoader

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize model on startup and handle cleanup."""
    try:
        model_loader = ModelLoader()
        await model_loader.load_model()
        yield
    except Exception as e:
        print(f"Error loading model: {e}")
        raise HTTPException(status_code=500, detail="Failed to load model")

def create_application() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description=settings.DESCRIPTION,
        lifespan=lifespan
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add API router
    app.include_router(api_router, prefix="/api/v1")

    return app

app = create_application()

@app.get("/health")
async def health_check():
    """Health check endpoint that verifies model is loaded and ready."""
    try:
        model = ModelLoader().model
        if not model:
            return {"status": "unhealthy", "detail": "Model not loaded"}
        
        return {
            "status": "healthy",
            "model": {
                "name": settings.MODEL_NAME,
            },
            "version": settings.VERSION
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "detail": str(e)
        }