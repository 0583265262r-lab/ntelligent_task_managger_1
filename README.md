<!-- **background** -->
An intelligence unit called ShadowNet needs a system to manage agents and missions.
<!-- **Folder structure** -->
intelligence-task-manager/
├── database/
│   ├── db_connection.py
│   ├── agent_db.py
│   └── mission_db.py
├── README.md
├── requirements.txt
└── .gitignore

<!-- Table structure -->
        <!-- agent_table -->
field   (type), (Comments)
ID	(INT, AUTO_INCREMENT, PK),(Unique identifier)
NAME	(VARCHAR(50)),(agent_name)
SPECIALTY	(VARCHAR(50)),(Field of specialization)
IS_ACTIVE	(BOOLEAN),(Default: TRUE)
COMPLETED_MISSIONS	(INT),(Default: 0)
FAILED_MISSIONS	(INT),	(Default: 0)
AGENT_RANK	(ENUM / VARCHAR),(Junior / Senior / Commander)

        <!-- missions_table -->
field   (type), (Comments)
ID	(INT, AUTO_INCREMENT, PK),(Unique identifier)
title	(VARCHAR(50)),(Mission title)
description	(TEXT)(Detailed description)
location	(VARCHAR(50))(Location)
difficulty	(INT),(1–10 only)	
importance	(INT),(1–10 only)
status	(VARCHAR(50)),(default:NEW)
risk_level	(VARCHAR(50)),(Automatically calculated — not coming from the user)
assigned_agent_id	(INT),(NULL until association)

    <!-- Calculating risk_level -->
<!-- 1-9 → LOW | 10–17 → MEDIUM | 18–24 → HIGH | 25+ → CRITICAL -->
**difficulty * 2 + importance = risk_level**

    <!-- missions_status -->
Status ,Meaning
NEW ,New task — default when created
ASSIGNED ,Assigned to agent
PROGRESS_IN ,In progress
COMPLETED ,Completed successfully
FAILED ,Failed
CANCELLED ,Canceled





<!-- class DBconnection -->
- method `get_connection()`
   - Returns an active connection to MYSQL
- method `create_database()`
   - Creates Intelligence_db if it does not exist.
- method `create_tables()` 
   - Creates both tables if they do not exist.

**Rule: Wherever it is not explicitly stated what to return, a success or failure message must be returned.**
<!-- class AgentDB -->
<!-- Responsible for all SQL operations against the agents table. -->
- method `create_agent(data)`
  - Creates a new agent and returns the agent object.
- method `get_all_agents()`
  - returns list of all agents
- method `get_agent_by_id(id)`
  - returns agent by ID or None
- method `update_agent(id, data)`
  - update for the entire row (cannot change id)
- method `deactivate_agent(id)`
  - Sets agent inactive status
- method `increment_completed(id)`
  - Updates the number of tasks completed.
- method `increment_failed(id)`
  - Updates the number of tasks failed.
- method `get_agent_performance(id)`
  - Returns a dictionary with these keys completed, failed, total, success_rate
    (success_rate - what percentage of tasks completed successfully out of the total)
- method `count_active_agents()`
  - returns number of active agents
<!-- class MissionDB -->
<!-- Responsible for all SQL operations against the missions table. -->
- method `create_mission(data)`
  - Creates a new task and returns the entire object
- method `get_all_missions()`
  - returns all missions
- method `get_mission_by_id(id)`
  - return one mission by ID or None
- method `assign_mission(m_id,a_id)`
  - Assigning a task to an agent
- method `update_mission_status(id, status)`
  - Used for any status change
- method `get_open_missions_by_agent(id)`
  - Returns agent ASSIGNED/IN_PROGRESS tasks
- method `count_all_missions()`
  - returns total tasks
- method `count_by_status(status)`
  - returns count of certain status
- method `count_open_missions()`
  - returns count of open missions
- method `count_critical_missions()`
  - returns count of CRITICAL tasks
- method `get_top_agent()`
  - returns the agent with the highest completed_missions.








<!-- System rules -->
1 rank must be Commander / Senior / Junior — any other value throws an error.
2 difficulty and importance must be between 1 and 10 — otherwise an error.
3 level_risk is calculated automatically when creating a task — the user does not send it.
4 An agent with False=active_is cannot accept tasks.
5 An agent cannot have more than 3 open tasks (PROGRESS_IN / ASSIGNED) at the same time.
6 If CRITICAL=level_risk — only an agent with the Commander rank can accept the task.
7 Only a task with the status NEW can be assigned. After assignment: ASSIGNED=status.
8 Only a task with the status ASSIGNED can be started. After: PROGRESS_IN=status.
9 Only a task with the status PROGRESS_IN can be finished and changed to completed or failed.
10 Only a task with the status NEW or ASSIGNED can be canceled — otherwise an error

<!-- Running instructions -->
Make a git clone of the repository
Set up a virtual environment
And run Docker
<!-- docker run -d --name intelligence-mysql -e MYSQL_ROOT_PASSWORD=1234 -e MYSQL_DATABASE=Intelligence_db -p 3306:3306 mysql:8.0 -->
And run the main file
