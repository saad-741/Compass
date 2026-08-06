from fastapi import APIRouter, HTTPException, status
from app.schemas.repository import QueryRequest, QuestionResponse, SourceCitationSchema
from app.utils.repo_utils import validate_and_parse_github_url
from app.services.qa_service import QAService

router = APIRouter(prefix="/api/chat", tags=["AI Q&A"])

@router.post("/query", response_model=QuestionResponse)
async def query_repository(payload: QueryRequest):
    
    try:
        owner, repo_name = validate_and_parse_github_url(payload.repo_url)
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))

    try:
        qa_result = QAService.answer_question(
            repo_owner=owner,
            repo_name=repo_name,
            query=payload.query,
            top_k=payload.top_k or 6
        )

        sources = [
            SourceCitationSchema(
                file_path=src.file_path,
                start_line=src.start_line,
                end_line=src.end_line,
                symbol=src.symbol
            )
            for src in qa_result.sources
        ]

        return QuestionResponse(
            question=payload.query,
            answer=qa_result.answer,
            sources=sources
        )

    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"AI Pipeline Error: {str(err)}")