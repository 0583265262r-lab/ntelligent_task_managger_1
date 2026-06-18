from fastapi import APIRouter,HTTPException,FastAPI
from database.db_connection import DBconnection
from database.agent_db import AgentDB
import uvicorn 
from routes import agent_routes,mission_routes,report_routes

agentdb= AgentDB()
connection = DBconnection()
app = FastAPI()
router= APIRouter()

app.include_router(agent_routes.router)
app.include_router(mission_routes.router)
app.include_router(report_routes.router)


if __name__ == "__main__":
    connection = DBconnection()
    uvicorn.run("main:app",reload=True,port=8000)
