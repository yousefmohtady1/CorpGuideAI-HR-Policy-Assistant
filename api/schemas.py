from pydantic import BaseModel
from typing import List, Optional, Tuple

class ChatRequest(BaseModel):
    question: str
    chat_history: List[Tuple[str,str]] = []

class ChatResponse(BaseModel):
    answer:str
    sources: List[str]
    latency: Optional[float] = None

class UploadResponse(BaseModel):
    filename: str
    chunks_count: int
    message:str