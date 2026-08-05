from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.ingest import router as ingest_router
from app.api.vectorstore import router as vectorstore_router
from app.api.qa import router as qa_router
from app.api.endpoints import router as api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AI-powered GitHub Repository Navigation Backend"
)

# Enable CORS for local development with React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict to standard Vite ports (e.g. http://localhost:5173) in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register main API routes
app.include_router(api_router)

# Register dev/testing routes
app.include_router(ingest_router)
app.include_router(vectorstore_router)
app.include_router(qa_router)

@app.get("/", tags=["Health"])
async def root():
    return {"message": "Compass Backend Running"}