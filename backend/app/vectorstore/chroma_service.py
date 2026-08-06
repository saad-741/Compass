import os
import chromadb
from chromadb.config import Settings as ChromaSettings
from sentence_transformers import SentenceTransformer
from app.core.config import settings
from app.services.chunking_service import CodeChunk

class VectorStoreService:
    _embedding_model = None
    _chroma_client = None

    @classmethod
    def get_embedding_model(cls) -> SentenceTransformer:
      
        # Loads all-MiniLM-L6-v2 model.
        if cls._embedding_model is None:
            cls._embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        return cls._embedding_model

    @classmethod
    def get_chroma_client(cls) -> chromadb.PersistentClient:

        # Initializes and returns a persistent ChromaDB client.
        if cls._chroma_client is None:
            os.makedirs(settings.CHROMA_PATH, exist_ok=True)
            cls._chroma_client = chromadb.PersistentClient(
                path=settings.CHROMA_PATH,
                settings=ChromaSettings(allow_reset=True, anonymized_telemetry=False)
            )
        return cls._chroma_client

    @classmethod
    def sanitize_collection_name(cls, repo_owner: str, repo_name: str) -> str:
 
        # ChromaDB collection names must be 3-63 chars, alphanumeric, containing '.' or '-'.
        clean_name = f"{repo_owner}-{repo_name}".lower()
        clean_name = "".join(c if c.isalnum() or c in ["-", "_"] else "-" for c in clean_name)
        clean_name = clean_name.strip("-_")
         
        if len(clean_name) < 3:
            clean_name = f"repo-{clean_name}"
        return clean_name[:63]

    @classmethod
    def store_chunks(cls, collection_name: str, chunks: list[CodeChunk]) -> int:

        # Generates embeddings for chunks and stores them in ChromaDB.
        if not chunks:
            return 0

        client = cls.get_chroma_client()
         
        collection = client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )

        model = cls.get_embedding_model()
        contents = [chunk.content for chunk in chunks]
        embeddings = model.encode(contents, batch_size=32, show_progress_bar=False).tolist()

        ids = [chunk.chunk_id for chunk in chunks]
        metadatas = [
            {
                "file_path": chunk.file_path,
                "language": chunk.language,
                "symbol": chunk.symbol or "",
                "start_line": chunk.start_line,
                "end_line": chunk.end_line
            }
            for chunk in chunks
        ]

        # Batch store in ChromaDB (batching by 100 to avoid limits)
        batch_size = 100
        for i in range(0, len(chunks), batch_size):
            collection.add(
                ids=ids[i:i + batch_size],
                embeddings=embeddings[i:i + batch_size],
                documents=contents[i:i + batch_size],
                metadatas=metadatas[i:i + batch_size]
            )

        return len(chunks)

    @classmethod
    def similarity_search(cls, collection_name: str, query: str, top_k: int = 5) -> list[dict]:

        client = cls.get_chroma_client()
        try:
            collection = client.get_collection(name=collection_name)
        except Exception:
            raise ValueError(f"Collection '{collection_name}' not found in vector database.")

        model = cls.get_embedding_model()
        query_embedding = model.encode([query]).tolist()

        results = collection.query(
            query_embeddings=query_embedding,
            n_results=top_k,
            include=["documents", "metadatas", "distances"]
        )

        search_results = []
        if results and results["ids"] and len(results["ids"][0]) > 0:
            for idx in range(len(results["ids"][0])):
                search_results.append({
                    "chunk_id": results["ids"][0][idx],
                    "content": results["documents"][0][idx],
                    "metadata": results["metadatas"][0][idx],
                    "score": round(1 - results["distances"][0][idx], 4)  # Convert cosine distance --> similarity score
                })

        return search_results