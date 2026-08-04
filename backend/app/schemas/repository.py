from pydantic import BaseModel, HttpUrl

class IngestRequest(BaseModel):
    repo_url: HttpUrl

class IngestResponse(BaseModel):
    task_id: str
    status: str
    message: str

class TaskStatusResponse(BaseModel):
    task_id: str
    status: str  # e.g., "processing", "completed", "failed"
    progress: str
    error: str | None = None