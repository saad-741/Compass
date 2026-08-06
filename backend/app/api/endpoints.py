from fastapi import APIRouter, BackgroundTasks, HTTPException, status
from app.schemas.repository import (
    IngestRequest,
    IngestTaskResponse,
    StatusResponse,
    ChatRequest,
    ChatResponse,
    SourceCitationSchema,
    RepositoryDetailsResponse
)
from app.services.task_service import TaskManager
from app.services.background_service import process_repository_task
from app.services.qa_service import QAService

router = APIRouter(prefix="/api", tags=["API Layer"])

# Endpoint 1: POST /api/ingest
@router.post("/ingest", response_model=IngestTaskResponse, status_code=status.HTTP_202_ACCEPTED)
async def ingest_repository(payload: IngestRequest, background_tasks: BackgroundTasks):

    # Initiates repos ingestion in the background and returns a task_id.  
    task_id = TaskManager.create_task()
    background_tasks.add_task(process_repository_task, task_id, payload.repo_url)
    return IngestTaskResponse(task_id=task_id)


# Endpoint 2: GET /api/status/{task_id}
@router.get("/status/{task_id}", response_model=StatusResponse)
async def get_task_status(task_id: str):

    # Returns the ingestion progress status and ready state.
    task_info = TaskManager.get_task(task_id)
    if not task_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task ID not found")

    is_ready = task_info.status == "completed"
    return StatusResponse(
        progress=task_info.progress,
        status=task_info.status,
        ready=is_ready,
        error=task_info.error
    )


# Endpoint 3: POST /api/chat
@router.post("/chat", response_model=ChatResponse)
async def chat_with_repository(payload: ChatRequest):

    repo_meta = TaskManager.get_repository(payload.repository_id)
    if not repo_meta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Repository not found or repository processing is not yet completed."
        )

    try:
        qa_result = QAService.answer_question(
            repo_owner=repo_meta.owner,
            repo_name=repo_meta.repo,
            query=payload.question,
            top_k=6
        )

        citations = [
            SourceCitationSchema(
                file_path=src.file_path,
                start_line=src.start_line,
                end_line=src.end_line,
                symbol=src.symbol
            )
            for src in qa_result.sources
        ]

        return ChatResponse(
            answer=qa_result.answer,
            citations=citations
        )
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err))


# Endpoint 4: GET /api/repository/{id}
@router.get("/repository/{repository_id}", response_model=RepositoryDetailsResponse)
async def get_repository_details(repository_id: str):

    # Returns metadata for an ingested repo.
    repo_meta = TaskManager.get_repository(repository_id)
    if not repo_meta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Repository ID not found")

    summary_text = (
        f"Repository {repo_meta.owner}/{repo_meta.repo} containing {repo_meta.total_files} "
        f"indexed source code files across languages: {', '.join(repo_meta.languages)}."
    )

    return RepositoryDetailsResponse(
        summary=summary_text,
        languages=repo_meta.languages,
        total_files=repo_meta.total_files,
        files=repo_meta.files,
        status=repo_meta.status
    )