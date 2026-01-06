from fastapi import APIRouter, HTTPException
from models.schemas import ChatRequest, ChatResponse
from services.rag_service import RAGService

router = APIRouter()
rag_service = RAGService()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        answer_data = rag_service.answer(request.question)

        return ChatResponse(
            answer=answer_data["answer"],
            sources=answer_data.get("sources", [])
        )

    except Exception as e:
        print(f"Error en /chat: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor"
        )
