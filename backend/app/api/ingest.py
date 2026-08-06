from fastapi import APIRouter, HTTPException, status
from app.schemas.repository import IngestRequest, IngestInspectResponse, FileSummary, ChunkInspectResponse
from app.utils.repo_utils import validate_and_parse_github_url
from app.services.ingestion_service import RepoIngestionService, IngestionError
from app.services.chunking_service import ChunkingService

# 1. Instantiate the router instance here
router = APIRouter(prefix="/api", tags=["Ingestion"])

# 2. Use @router.post (NOT @APIRouter().post)
@router.post("/ingest/test", response_model=IngestInspectResponse)
async def test_repository_ingestion(payload: IngestRequest):
    
    # Validate URL
    try:
        owner, repo_name = validate_and_parse_github_url(payload.repo_url)
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))

    # Clone Repository
    try:
        repo_id, repo_path = RepoIngestionService.clone_repository(payload.repo_url)
    except IngestionError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))

    try: 
        valid_files = RepoIngestionService.validate_and_filter_repository(repo_path)
         
        file_summaries = [
            FileSummary(
                relative_path=str(f.relative_to(repo_path)).replace("\\", "/"),
                extension=f.suffix.lower()
            )
            for f in valid_files
        ]

        return IngestInspectResponse(
            repo_id=repo_id,
            owner=owner,
            repo=repo_name,
            total_files_found=len(file_summaries),
            files=file_summaries[:20],
            message="Repository successfully cloned, validated, and filtered."
        )

    except IngestionError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))

    finally: 
        RepoIngestionService.cleanup_repository(repo_path)


@router.post("/chunk/test", response_model=ChunkInspectResponse)
async def test_repository_chunking(payload: IngestRequest):
    
    try:
        owner, repo_name = validate_and_parse_github_url(payload.repo_url)
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))

    try:
        repo_id, repo_path = RepoIngestionService.clone_repository(payload.repo_url)
    except IngestionError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))

    try:
        valid_files = RepoIngestionService.validate_and_filter_repository(repo_path)
        
        # Phase 3: Perform chunking
        chunks = ChunkingService.process_repository(valid_files, repo_path)

        sample = [chunk.model_dump() for chunk in chunks[:5]]

        return ChunkInspectResponse(
            repo_id=repo_id,
            owner=owner,
            repo=repo_name,
            total_files_processed=len(valid_files),
            total_chunks_generated=len(chunks),
            sample_chunks=sample
        )

    except IngestionError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))

    finally:
        RepoIngestionService.cleanup_repository(repo_path)