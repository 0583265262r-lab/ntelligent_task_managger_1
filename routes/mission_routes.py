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
    if not missiondb.risk_level_critical(id,agent_id):
         raise HTTPException(status_code=400,detail="Only a Commander-ranked agent can accept the mission.")
    missiondb.assign_mission(id,agent_id)
    return "ASSIGNED"
@router.put("/missions/{id}/start")
def start_mission(id:int):
    if not missiondb.get_mission_by_id(id):
        raise HTTPException(status_code=404,detail="mission not found")
    if missiondb.get_mission_by_id(id)["status"]!="assigned":
        raise HTTPException(status_code=400)
    missiondb.update_mission_status(id,"in_progress")
    return {"mission":id,"status":"in_progress"}
@router.put("/missions/{id}/complete")
def complete_mission(id:int):
    if not missiondb.get_mission_by_id(id):
       raise HTTPException(status_code=404,detail="mission not found")
    if missiondb.get_mission_by_id(id)["status"]!="in_progress":
        raise HTTPException(status_code=400)
    missiondb.update_mission_status(id,"completed")
    agentdb.increment_completed(missiondb.get_mission_by_id(id)["assigned_agent_id"])
    return {"mission":id,"status":"completed"}
@router.put("/missions/{id}/fail")
def failed_mission(id:int):
    if not missiondb.get_mission_by_id(id):
       raise HTTPException(status_code=404,detail="mission not found")
    if missiondb.get_mission_by_id(id)["status"]!="in_progress":
        raise HTTPException(status_code=400)
    missiondb.update_mission_status(id,"failed")
    agentdb.increment_failed(missiondb.get_mission_by_id(id)["assigned_agent_id"])
    return {"mission":id,"status":"failed"}
@router.put("/missions/{id}/cancel")
def canceled_mission(id:int):
    if not missiondb.get_mission_by_id(id):
       raise HTTPException(status_code=404,detail="mission not found")
    if missiondb.get_mission_by_id(id)["status"]!="assigned" and missiondb.get_mission_by_id(id)["status"]!="new":
        raise HTTPException(status_code=400)
    missiondb.update_mission_status(id,"cancelled")
    return {"mission":id,"status":"cancelled"}

    


