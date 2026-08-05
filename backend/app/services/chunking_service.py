import uuid
from pathlib import Path
from typing import Optional
from pydantic import BaseModel
from langchain_text_splitters import Language, RecursiveCharacterTextSplitter

# Map file extensions to LangChain supported languages
EXTENSION_TO_LANGUAGE = {
    ".py": Language.PYTHON,
    ".js": Language.JS,
    ".jsx": Language.JS,
    ".ts": Language.TS,
    ".tsx": Language.TS,
    ".java": Language.JAVA,
    ".cpp": Language.CPP,
    ".go": Language.GO,
    ".html": Language.HTML,
    ".md": Language.MARKDOWN,
}

class CodeChunk(BaseModel):
    chunk_id: str
    content: str
    file_path: str
    language: str
    symbol: Optional[str] = None
    start_line: int
    end_line: int

class ChunkingService:

    @staticmethod
    def _detect_language(file_extension: str) -> Optional[Language]:
        """Maps file extension to LangChain Language enum."""
        return EXTENSION_TO_LANGUAGE.get(file_extension.lower())

    @staticmethod
    def _calculate_line_numbers(full_content: str, chunk_content: str, search_start_index: int = 0) -> tuple[int, int, int]:
        """
        Calculates 1-based start_line and end_line for a chunk within the full text.
        Returns (start_line, end_line, new_search_index).
        """
        start_char_idx = full_content.find(chunk_content, search_start_index)
        if start_char_idx == -1:
            # Fallback if exact match isn't found sequentially
            start_char_idx = search_start_index

        start_line = full_content.count('\n', 0, start_char_idx) + 1
        chunk_lines = chunk_content.count('\n')
        end_line = start_line + chunk_lines

        return start_line, end_line, start_char_idx + len(chunk_content)

    @staticmethod
    def parse_and_chunk_file(file_path: Path, repo_root: Path) -> list[CodeChunk]:
        """
        Reads a single file, applies structural or recursive chunking,
        extracts line ranges, and constructs enriched CodeChunk objects.
        """
        relative_path = str(file_path.relative_to(repo_root)).replace("\\", "/")
        extension = file_path.suffix.lower()
        language_enum = ChunkingService._detect_language(extension)
        language_str = language_enum.value if language_enum else extension.lstrip(".")

        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                full_content = f.read()
        except Exception:
            return []

        if not full_content.strip():
            return []

        # Configure splitter: Prefer AST/language syntax boundaries if supported
        if language_enum:
            splitter = RecursiveCharacterTextSplitter.from_language(
                language=language_enum,
                chunk_size=1000,
                chunk_overlap=150
            )
        else:
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=150
            )

        raw_chunks = splitter.split_text(full_content)
        code_chunks: list[CodeChunk] = []
        search_idx = 0

        for chunk_text in raw_chunks:
            if not chunk_text.strip():
                continue

            start_line, end_line, search_idx = ChunkingService._calculate_line_numbers(
                full_content=full_content,
                chunk_content=chunk_text,
                search_start_index=search_idx
            )

            # Generate unique chunk ID (Step 5)
            chunk_id = f"{relative_path}::{start_line}-{end_line}::{uuid.uuid4().hex[:8]}"

            # Detect top symbol (e.g. function/class declaration) if present in first line
            first_line = chunk_text.strip().split("\n")[0]
            symbol = first_line[:60] if any(kw in first_line for kw in ["def ", "class ", "function ", "const ", "interface "]) else None

            code_chunks.append(
                CodeChunk(
                    chunk_id=chunk_id,
                    content=chunk_text,
                    file_path=relative_path,
                    language=language_str,
                    symbol=symbol,
                    start_line=start_line,
                    end_line=end_line
                )
            )

        return code_chunks

    @classmethod
    def process_repository(cls, file_paths: list[Path], repo_root: Path) -> list[CodeChunk]:
        """
        Iterates over all filtered repository files and processes them into chunks.
        """
        all_chunks: list[CodeChunk] = []
        for file_path in file_paths:
            chunks = cls.parse_and_chunk_file(file_path, repo_root)
            all_chunks.extend(chunks)
        return all_chunks