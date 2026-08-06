import os
from groq import Groq
from pydantic import BaseModel
from app.core.config import settings
from app.vectorstore.chroma_service import VectorStoreService
from app.prompts.qa_prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE

class SourceCitation(BaseModel):
    file_path: str
    start_line: int
    end_line: int
    symbol: str

class QAResponse(BaseModel):
    answer: str
    sources: list[SourceCitation]

class QAService:
    _groq_client = None

    @classmethod
    def get_groq_client(cls) -> Groq:
        """Loads and caches the Groq API client."""
        if cls._groq_client is None:
            api_key = settings.GROQ_API_KEY
            if not api_key:
                raise ValueError("GROQ_API_KEY environment variable is not set in .env")
            cls._groq_client = Groq(api_key=api_key)
        return cls._groq_client

    @classmethod
    def answer_question(
        cls, 
        repo_owner: str, 
        repo_name: str, 
        query: str, 
        top_k: int = 6
    ) -> QAResponse:
        
        collection_name = VectorStoreService.sanitize_collection_name(repo_owner, repo_name)

        retrieved_chunks = VectorStoreService.similarity_search(
            collection_name=collection_name,
            query=query,
            top_k=top_k
        )

        if not retrieved_chunks:
            return QAResponse(
                answer="No relevant code or documentation chunks found in this repository to answer your question.",
                sources=[]
            )

        context_blocks = []
        sources: list[SourceCitation] = []
        seen_sources = set()

        for idx, chunk in enumerate(retrieved_chunks, 1):
            meta = chunk["metadata"]
            file_path = meta.get("file_path", "Unknown")
            start_line = meta.get("start_line", 0)
            end_line = meta.get("end_line", 0)
            symbol = meta.get("symbol", "")

            block = (
                f"--- Chunk {idx} ---\n"
                f"File: {file_path} (Lines {start_line}-{end_line})\n"
                f"Symbol: {symbol if symbol else 'N/A'}\n"
                f"Code:\n{chunk['content']}\n"
            )
            context_blocks.append(block)

            source_key = f"{file_path}::{start_line}-{end_line}"
            if source_key not in seen_sources:
                seen_sources.add(source_key)
                sources.append(
                    SourceCitation(
                        file_path=file_path,
                        start_line=start_line,
                        end_line=end_line,
                        symbol=symbol
                    )
                )

        context_str = "\n".join(context_blocks)

        formatted_system_prompt = SYSTEM_PROMPT.format(context_str=context_str)
        formatted_user_prompt = USER_PROMPT_TEMPLATE.format(query=query)

        client = cls.get_groq_client()
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": formatted_system_prompt},
                {"role": "user", "content": formatted_user_prompt}
            ],
            temperature=0.2,   
            max_tokens=2048
        )

        answer_text = completion.choices[0].message.content

        return QAResponse(
            answer=answer_text,
            sources=sources
        )