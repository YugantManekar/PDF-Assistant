from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    session_id: str
    question: str

class ChatResponse(BaseModel):
    answer: str
    translated_answer: Optional[str] = None

class TTSRequest(BaseModel):
    text: str
    language: str
