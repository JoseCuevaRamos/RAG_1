from pydantic import BaseModel


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[str] = []


class DocumentUpload(BaseModel):
    filename: str
    content: bytes