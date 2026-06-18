from fastapi import APIRouter,HTTPException,FastAPI
from database.agent_db import AgentDB
from database.mission_db import MissionDB
import uvicorn
from pydantic import BaseModel
agentdb= AgentDB()
missiondb = MissionDB()
router = APIRouter()

class MissionIn(BaseModel):
    title: str
    description:str
    location:str
    difficulty:int
    importance:int


@router.post("/missions")
def create_mission(body:MissionIn):
    data =  body.model_dump()
    return missiondb.create_mission(data)
@router.get("/missions")
def get_all_mission():
    return missiondb.get_all_missions()
@router.get("/missions/{id}")
def get_mission_by_id(id:int):
    if not missiondb.get_mission_by_id(id):
        raise HTTPException(status_code=404,detail="mission not found")
    return missiondb.get_mission_by_id(id)
@router.put("/missions/{id}/assign/{agent_id}")
def assign_mission(id:int,agent_id:int):
    if not missiondb.get_mission_by_id(id):
        raise HTTPException(status_code=404,detail="mission not found")
    if not agentdb.get_agent_by_id(agent_id):
        raise HTTPException(status_code=404,detail="id not found ")
    if not agentdb.exist_and_active_agent(agent_id):
        raise HTTPException(status_code=400,detail="Agent is not active")
    if missiondb.get_mission_by_id(id)["status"] != "new":
            raise HTTPException(status_code=400,detail="Mission not available")
    if len(missiondb.get_open_missions_by_agent(agent_id)) >=3:
            raise HTTPException(status_code=400,detail="Agent has reached maximum missions")
    if not missiondb.risk_level_critical(m_id,a_id):
    
    missiondb.assign_mission(id,agent_id)
    

