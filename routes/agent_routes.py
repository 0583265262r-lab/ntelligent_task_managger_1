from fastapi import APIRouter,HTTPException,FastAPI
from database.agent_db import AgentDB
import uvicorn
from pydantic import BaseModel
import logging
from routes.logger import logger
agentdb= AgentDB()
router = APIRouter()
class AgentIn(BaseModel):
    name: str 
    specialty: str
    agent_rank: str
@router.post("/agents")
def create_agent(body:AgentIn):
    logger.info("POST | create agent")
    data = body.model_dump()
    logger.info("POsT |Agent created successfully")
    return agentdb.create_agent(data)

@router.get("/agents")
def get_all_agents():
    return agentdb.get_all_agents()

@router.get("/agents/{id}")
def get_agent_by_id(id:int):
    if not agentdb.get_agent_by_id(id):
        raise HTTPException(status_code=404,detail="id not found ")
    return agentdb.get_agent_by_id(id)
class UpdateIn(BaseModel):
    name: str | None = None
    specialty: str | None = None
    agent_rank: str | None = None
    is_active: bool | None = None
    
@router.put("/agents/{id}")
def update_agent(id:int,body:UpdateIn):
    if not agentdb.get_agent_by_id(id):
        raise HTTPException(status_code=404,detail="id not found ")
    data = body.model_dump(exclude_unset=True)
    print(data)
    return agentdb.update_agent(id,data)
@router.put("/agents/{id}/deactivate")
def deactivate_agent(id:int):
    if not agentdb.get_agent_by_id(id):
        raise HTTPException(status_code=404,detail="id not found ")
    return agentdb.deactivate_agent(id)
@router.get("/agents/{id}/performance")
def get_agent_performance(id:int):
    if not agentdb.get_agent_by_id(id):
        raise HTTPException(status_code=404,detail="id not found ")
    return agentdb.get_agent_performance(id)

   

