import uuid
from typing import Optional, Dict
from pydantic import BaseModel

class TaskStatus(BaseModel):
    task_id: str
    status: str  # "processing", "completed", "failed"
    progress: str  # Progress step description (e.g., "Cloning repository...")
    repo_owner: Optional[str] = None
    repo_name: Optional[str] = None
    error: Optional[str] = None

class RepositorySummary(BaseModel):
    repository_id: str
    owner: str
    repo: str
    total_files: int
    languages: list[str]
    files: list[str]
    status: str

# Global in-memory stores
TASKS_DB: Dict[str, TaskStatus] = {}
REPOSITORIES_DB: Dict[str, RepositorySummary] = {}

class TaskManager:
    @classmethod
    def create_task(cls) -> str:
        import uuid
        task_id = str(uuid.uuid4())
        TASKS_DB[task_id] = TaskStatus(
            task_id=task_id,
            status="processing",
            progress="Initializing repository ingestion..."
        )
        return task_id

    @classmethod
    def update_task(
        cls, 
        task_id: str, 
        progress: str, 
        status: str = "processing", 
        repo_owner: Optional[str] = None, 
        repo_name: Optional[str] = None,
        error: Optional[str] = None
    ) -> None:
        if task_id in TASKS_DB:
            TASKS_DB[task_id].progress = progress
            TASKS_DB[task_id].status = status
            if repo_owner:
                TASKS_DB[task_id].repo_owner = repo_owner
            if repo_name:
                TASKS_DB[task_id].repo_name = repo_name
            if error:
                TASKS_DB[task_id].error = error

    @classmethod
    def get_task(cls, task_id: str) -> Optional[TaskStatus]:
        return TASKS_DB.get(task_id)

    @classmethod
    def register_repository(
        cls,
        task_id: str,
        owner: str,
        repo: str,
        total_files: int,
        languages: list[str],
        files: list[str]
    ) -> None:
        REPOSITORIES_DB[task_id] = RepositorySummary(
            repository_id=task_id,
            owner=owner,
            repo=repo,
            total_files=total_files,
            languages=languages,
            files=files,
            status="ready"
        )

    @classmethod
    def get_repository(cls, repo_id: str) -> Optional[RepositorySummary]:
        return REPOSITORIES_DB.get(repo_id)


# class TaskManager:
#     _tasks: Dict[str, TaskStatus] = {}
#     _repositories: Dict[str, RepositorySummary] = {}

#     @classmethod
#     def create_task(cls) -> str:
#         task_id = str(uuid.uuid4())
#         cls._tasks[task_id] = TaskStatus(
#             task_id=task_id,
#             status="processing",
#             progress="Initializing repository ingestion..."
#         )
#         return task_id

#     @classmethod
#     def update_task(
#         cls, 
#         task_id: str, 
#         progress: str, 
#         status: str = "processing", 
#         repo_owner: Optional[str] = None, 
#         repo_name: Optional[str] = None,
#         error: Optional[str] = None
#     ) -> None:
#         if task_id in cls._tasks:
#             cls._tasks[task_id].progress = progress
#             cls._tasks[task_id].status = status
#             if repo_owner:
#                 cls._tasks[task_id].repo_owner = repo_owner
#             if repo_name:
#                 cls._tasks[task_id].repo_name = repo_name
#             if error:
#                 cls._tasks[task_id].error = error

#     @classmethod
#     def get_task(cls, task_id: str) -> Optional[TaskStatus]:
#         return cls._tasks.get(task_id)

#     @classmethod
#     def register_repository(
#         cls,
#         task_id: str,
#         owner: str,
#         repo: str,
#         total_files: int,
#         languages: list[str],
#         files: list[str]
#     ) -> None:
#         cls._repositories[task_id] = RepositorySummary(
#             repository_id=task_id,
#             owner=owner,
#             repo=repo,
#             total_files=total_files,
#             languages=languages,
#             files=files,
#             status="ready"
#         )

#     @classmethod
#     def get_repository(cls, repo_id: str) -> Optional[RepositorySummary]:
#         return cls._repositories.get(repo_id)

    