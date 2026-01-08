from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.service.agent_service import AgentService
from app.service.vector_service import VectorService
from app.deps import get_agent_service, get_vector_service

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

#채팅 기능
@router.post("/chat")
def chat(request: ChatRequest, service: AgentService = Depends(get_agent_service)):
    answer = service.process_query(request.message)
    return {"ai_message": answer}

#지식 주입 기능
@router.post("/knowledge")
def load_knowledge(service: VectorService = Depends(get_vector_service)):
    result = service.save_documents("rules.json")
    return {"status": "OK", "detail": result}