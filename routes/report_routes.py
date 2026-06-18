from fastapi import APIRouter,HTTPException,FastAPI
from database.agent_db import AgentDB
from database.mission_db import MissionDB
import uvicorn
from pydantic import BaseModel
agentdb= AgentDB()
missiondb = MissionDB()
router = APIRouter()

@router.get("/reports/summary")
def general_reports():
    general = {"active_agents_count":agentdb.count_active_agents()["active_agents"],
               "total_missions":missiondb.count_all_missions()["Total missions"],
               "open_missions":missiondb.count_open_missions()["open_missions"],
               "completed_missions":missiondb.count_by_status("completed")["mission_status"],
               "failed_missions":missiondb.count_by_status("failed")["mission_status"],
               "cancelled_missions":missiondb.count_by_status("cancelled")["mission_status"]}
    return general
@router.get("/reports/missions-by-status")
def get_missions_by_status():
    missions = {"open":(missiondb.count_by_status("new")["mission_status"] + missiondb.count_by_status("assigned")["mission_status"]),
                "in_progress":missiondb.count_by_status("in_progress")["mission_status"],
                "completed":missiondb.count_by_status("completed")["mission_status"],
                "failed":missiondb.count_by_status("failed")["mission_status"],
                "canceled":missiondb.count_by_status("cancelled")["mission_status"]}
    return missions
@router.get("/reports/top-agent")
def get_top_agents():
    if not missiondb.get_top_agent():
        raise HTTPException(status_code=404,detail="no top agent")
    return missiondb.get_top_agent()
