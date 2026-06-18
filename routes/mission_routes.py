from fastapi import APIRouter,HTTPException,FastAPI
from database.agent_db import AgentDB
from database.mission_db import MissionDB
import uvicorn
from pydantic import BaseModel
agentdb= AgentDB()
missiondb = MissionDB()
router = APIRouter()
