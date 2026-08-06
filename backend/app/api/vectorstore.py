from fastapi import APIRouter, HTTPException, status
from app.schemas.repository import (
    IngestRequest, 
    QueryRequest, 
    VectorStoreInspectResponse, 
    SearchResponse,
    SearchResultItem
)
from app.utils.repo_utils import validate_and_parse_github_url
from app.services.ingestion_service import RepoIngestionService, IngestionError
from app.services.chunking_service import ChunkingService
from app.vectorstore.chroma_service import VectorStoreService

router = APIRouter(prefix="/api/vectorstore", tags=["Vector Store"])

@router.post("/index", response_model=VectorStoreInspectResponse)
async def index_repository(payload: IngestRequest):
    
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
        chunks = ChunkingService.process_repository(valid_files, repo_path)
        
        collection_name = VectorStoreService.sanitize_collection_name(owner, repo_name)
        indexed_count = VectorStoreService.store_chunks(collection_name, chunks)

        return VectorStoreInspectResponse(
            collection_name=collection_name,
            owner=owner,
            repo=repo_name,
            total_chunks_indexed=indexed_count,
            message=f"Successfully indexed {indexed_count} chunks into ChromaDB collection '{collection_name}'."
        )

    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err))

    finally:
        RepoIngestionService.cleanup_repository(repo_path)


@router.post("/search", response_model=SearchResponse)
async def search_vectorstore(payload: QueryRequest):
    
    try:
        owner, repo_name = validate_and_parse_github_url(payload.repo_url)
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))

    collection_name = VectorStoreService.sanitize_collection_name(owner, repo_name)

    try:
        results = VectorStoreService.similarity_search(
            collection_name=collection_name,
            query=payload.query,
            top_k=payload.top_k or 5
        )

        search_items = [
            SearchResultItem(
                chunk_id=res["chunk_id"],
                content=res["content"],
                metadata=res["metadata"],
                score=res["score"]
            )
            for res in results
        ]

        return SearchResponse(
            collection_name=collection_name,
            query=payload.query,
            results_count=len(search_items),
            results=search_items
        )

    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err))