from fastapi import Depends
from app.service.time_service import TimeService
from app.core.db import get_db_client
from app.repository.vector_repo import VectorRepository
from app.service.vector_service import VectorService
from app.service.agent_service import AgentService

#TimeService
def get_time_service() -> TimeService:
    return TimeService()

def get_vector_repo(client = Depends(get_db_client)) -> VectorRepository:
    return VectorRepository(client)

def get_vector_service(repo: VectorRepository = Depends(get_vector_repo)) -> VectorService:
    return VectorService(repo)

def get_agent_service(
    time_service: TimeService = Depends(get_time_service),
    vector_service: VectorService = Depends(get_vector_service)
) -> AgentService:
    return AgentService(time_service, vector_service)