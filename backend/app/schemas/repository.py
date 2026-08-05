from typing import Optional, List
from pydantic import BaseModel

class IngestRequest(BaseModel):
    repo_url: str

class IngestTaskResponse(BaseModel):
    task_id: str

class StatusResponse(BaseModel):
    progress: str
    status: str
    ready: bool
    error: Optional[str] = None

class ChatRequest(BaseModel):
    repository_id: str
    question: str

class QueryRequest(BaseModel):
    repo_url: str
    query: str
    top_k: Optional[int] = 6

class SourceCitationSchema(BaseModel):
    file_path: str
    start_line: int
    end_line: int
    symbol: str

class ChatResponse(BaseModel):
    answer: str
    citations: List[SourceCitationSchema]

class RepositoryDetailsResponse(BaseModel):
    summary: str
    languages: List[str]
    total_files: int
    files: List[str]
    status: str

class QuestionResponse(BaseModel):
    question: str
    answer: str
    sources: list[SourceCitationSchema]

class FileSummary(BaseModel):
    relative_path: str
    extension: str

class IngestInspectResponse(BaseModel):
    repo_id: str
    owner: str
    repo: str
    total_files_found: int
    files: list[FileSummary]
    message: str

class ChunkInspectResponse(BaseModel):
    repo_id: str
    owner: str
    repo: str
    total_files_processed: int
    total_chunks_generated: int
    sample_chunks: list[dict]

 
class VectorStoreInspectResponse(BaseModel):
    collection_name: str
    owner: str
    repo: str
    total_chunks_indexed: int
    message: str

class SearchResultItem(BaseModel):
    chunk_id: str
    content: str
    metadata: dict
    score: float

class SearchResponse(BaseModel):
    collection_name: str
    query: str
    results_count: int
    results: list[SearchResultItem]