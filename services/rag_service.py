from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.messages import SystemMessage, HumanMessage
from core.config import settings
from services.vector_service import VectorService
import asyncio


class RAGService:
    def __init__(self):
        self.vector_service = VectorService()

        self.llm = ChatOpenAI(
            model=settings.CHAT_MODEL,
            api_key=settings.OPENAI_API_KEY,
            temperature=0
        )

        self.embedding_model = OpenAIEmbeddings(
            model="text-embedding-3-small",
            api_key=settings.OPENAI_API_KEY
        )

    def search(self, query: str, limit: int = 3):
        query_vector = self.embedding_model.embed_query(query)

        return self.vector_service.client.search(
            collection_name=self.vector_service.collection_name,
            query_vector=query_vector,  
            limit=limit,
            with_payload=True
        )



    def answer(self, question: str):
        results = self.search(question)

        if not results:
            return {
                "answer": "Lo siento, no pude encontrar información relevante para responder a tu pregunta.",
                "sources": []
            }

        context_text = "\n\n".join(
            res.payload.get("text", "") for res in results
        )

        system_prompt = f"""
Eres un asistente experto en analizar documentos.
Responde ÚNICAMENTE con base en el contexto.
Si no está en el contexto, di que no lo sabes.

CONTEXTO:
{context_text}
"""

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=question)
        ]

        ai_response = self.llm.invoke(messages)

        sources = list({
            res.payload.get("metadata", {}).get("source", "Desconocido")
            for res in results
        })

        return {
            "answer": ai_response.content,
            "sources": sources
        }


# Wrapper async para FastAPI
async def answer_question(question: str):
    rag = RAGService()
    result = await asyncio.to_thread(rag.answer, question)

    if isinstance(result, dict):
        return result.get("answer", ""), result.get("sources", [])

    return str(result), []
