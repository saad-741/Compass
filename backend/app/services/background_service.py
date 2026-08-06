import traceback
from app.utils.repo_utils import validate_and_parse_github_url
from app.services.ingestion_service import RepoIngestionService, IngestionError
from app.services.chunking_service import ChunkingService
from app.vectorstore.chroma_service import VectorStoreService
from app.services.task_service import TaskManager

def process_repository_task(task_id: str, repo_url: str) -> None:
    
    try:
        # Validate URL
        TaskManager.update_task(task_id, "Validating repository URL...")
        owner, repo_name = validate_and_parse_github_url(repo_url)
        TaskManager.update_task(task_id, "Cloning repository...", repo_owner=owner, repo_name=repo_name)

        # Shallow clone repo
        _, repo_path = RepoIngestionService.clone_repository(repo_url)

        try:
            # Filter supported files
            TaskManager.update_task(task_id, "Filtering source files...")
            valid_files = RepoIngestionService.validate_and_filter_repository(repo_path)
            
            # Extract language extensions and file paths
            languages = sorted(list({f.suffix.lower().lstrip(".") for f in valid_files if f.suffix}))
            relative_files = [str(f.relative_to(repo_path)).replace("\\", "/") for f in valid_files]

            # Chunk code
            TaskManager.update_task(task_id, f"Parsing and chunking {len(valid_files)} source files...")
            chunks = ChunkingService.process_repository(valid_files, repo_path)

            # Store in ChromaDB
            TaskManager.update_task(task_id, f"Generating embeddings for {len(chunks)} code chunks...")
            collection_name = VectorStoreService.sanitize_collection_name(owner, repo_name)
            VectorStoreService.store_chunks(collection_name, chunks)

            # Register repository metadata
            TaskManager.register_repository(
                task_id=task_id,
                owner=owner,
                repo=repo_name,
                total_files=len(valid_files),
                languages=languages,
                files=relative_files
            )
 
            TaskManager.update_task(task_id, "Repository ready!", status="completed")

        finally:
            # Cleanup temporary clone folder
            RepoIngestionService.cleanup_repository(repo_path)

    except IngestionError as err:
        TaskManager.update_task(task_id, "Failed", status="failed", error=str(err))
    except Exception as err:
        TaskManager.update_task(task_id, "Failed", status="failed", error=f"Internal processing error: {str(err)}")