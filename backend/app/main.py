from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

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

@app.get("/", tags=["Health"])
async def root():
    return {"message": "Compass Backend Running"}