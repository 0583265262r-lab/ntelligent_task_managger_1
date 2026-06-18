from database.db_connection import DBconnection
from database.agent_db import AgentDB
agentdb= AgentDB()
connection = DBconnection()

 
class MissionDB:
    def create_mission(self,data:dict):
        conn = connection.get_connection()
        cursor  = conn.cursor(dictionary=True)
        if  data["difficulty"] < 1 or  data["difficulty"] > 10 :
            if data["importance"] < 1 or  data["importance"] > 10 :
                raise ValueError ("please enter number between 1-10 only")
            raise ValueError ("please enter number between 1-10 only")
        level_risk = self.risk_level(data)
        query = "INSERT INTO missions (title, description, location,difficulty,importance,risk_level) VALUES (%s,%s,%s,%s,%s,%s)"
        val =list(data.values())+[level_risk]
        cursor.execute(query,(val))
        conn.commit()
        agent = cursor.lastrowid
        conn.close()
        cursor.close()
        return self.get_mission_by_id(agent)
    def risk_level(self,data:dict):
        ''' helping func '''
        risk_level_calculation = (data["difficulty"] *2) + data["importance"]
        if 1 < risk_level_calculation < 9:
            return "low"
        if 10 < risk_level_calculation < 17:
            return "medium"
        if 18 < risk_level_calculation < 24:
            return "high"
        if risk_level_calculation >= 25 :
            return "critical"
    def get_all_missions(self):
        conn = connection.get_connection()
        cursor  = conn.cursor(dictionary=True)
        query = "SELECT * FROM missions"
        cursor.execute(query)
        all_agents = cursor.fetchall()
        conn.close()
        cursor.close()
        return all_agents
    def get_mission_by_id(self,id:int):
        conn = connection.get_connection()
        cursor  = conn.cursor(dictionary=True)
        query = "SELECT * FROM missions WHERE id = %s"
        cursor.execute(query,(id,))
        mission = cursor.fetchone()
        conn.close()
        cursor.close()
        if not mission:
            return None
        return mission
    def assign_mission(self,m_id,a_id):
        if self.get_mission_by_id(m_id)["status"] != "new":
            raise ValueError("The mission has already been assigned.")
        agentdb.exist_and_active_agent(a_id)
        self.risk_level_critical(m_id,a_id)
        if len(self.get_open_missions_by_agent(a_id)) >=3:
            raise ValueError("The agent has reached maximum missions.")
        if not self.get_mission_by_id(m_id):
            raise ValueError ('mission not found')
        
        conn = connection.get_connection()
        cursor  = conn.cursor(dictionary=True)
        query = "UPDATE missions SET status = 'assigned' ,assigned_agent_id = %s WHERE id = %s "
        val = [a_id] + [m_id]
        cursor.execute(query,val)
        conn.commit()
        changed = cursor.rowcount > 0
        conn.close()
        cursor.close()
        return changed
    def update_mission_status(self,id, status):
        mission_status = {'new','assigned','in_progress','completed','failed','cancelled'}
        if not self.get_mission_by_id(id):
            raise ValueError ('mission not found')
        conn = connection.get_connection()
        cursor  = conn.cursor(dictionary=True)
        if status not in mission_status:
            raise ValueError ("incorrect status")
        query = "UPDATE missions SET status = %s WHERE id = %s"
        val = [status] + [id]
        cursor.execute(query,val)
        conn.commit()
        changed = cursor.rowcount > 0
        conn.close()
        cursor.close()
        return changed

    def get_open_missions_by_agent(self,id):
        if not agentdb.get_agent_by_id(id):
            raise ValueError ('mission not found')
        conn = connection.get_connection()
        cursor  = conn.cursor(dictionary=True)
        query = "SELECT * FROM missions WHERE assigned_agent_id = %s AND (status = 'in_progress' OR status = 'assigned')"
        cursor.execute(query,(id,))
        mission_of_agent = cursor.fetchall()
        conn.close()
        cursor.close()
        return mission_of_agent

    def count_all_missions(self):
        all_missions = self.get_all_missions()
        return {"Total missions":len(all_missions)}
    def count_by_status(self,status):
        mission_status = {'new','assigned','in_progress','completed','failed','cancelled'}
        if status not in mission_status:
            raise ValueError ("incorrect status")
        conn = connection.get_connection()
        cursor  = conn.cursor(dictionary=True)
        query = "SELECT COUNT(*) AS mission_status FROM missions WHERE status = %s"
        cursor.execute(query,(status,))
        status_count = cursor.fetchone()
        conn.close()
        cursor.close()
        return status_count
    def count_open_missions(self):
        conn = connection.get_connection()
        cursor  = conn.cursor(dictionary=True)
        query = "SELECT COUNT(*) AS open_missions FROM missions WHERE (status = 'in_progress' OR status = 'assigned') "
        cursor.execute(query)
        open_missions = cursor.fetchone()
        conn.close()
        cursor.close()
        return open_missions
    def count_critical_missions(self):
        conn = connection.get_connection()
        cursor  = conn.cursor(dictionary=True)
        query = "SELECT COUNT(*) AS critical_missions FROM missions WHERE (risk_level = 'critical') "
        cursor.execute(query)
        critical_missions = cursor.fetchone()
        conn.close()
        cursor.close()
        return critical_missions
    def get_top_agent(self):
        conn = connection.get_connection()
        cursor  = conn.cursor(dictionary=True)
        query = "SELECT * FROM agents ORDER BY completed_missions DESC LIMIT 1"
        cursor.execute(query)
        top_agent = cursor.fetchone()
        conn.close()
        cursor.close()
        return top_agent

    def risk_level_critical(self,m_id,a_id):
        if self.get_mission_by_id(m_id)["risk_level"] == 'critical':
            if agentdb.get_agent_by_id(a_id)["agent_rank"]!="Commander":
                raise ValueError("Only a Commander-ranked agent can accept the mission.")
    # def status_update_rules(self,id,status):
    #     current_mission = self.get_mission_by_id(id)
    #     if status == "assigned":
    #     pass


        
if __name__ == "__main__":
    c1 = MissionDB()
    # print(c1.create_mission({"title":"ydeg","description":'ghg','location':'ggg','difficulty':758,'importance':9}))
    # print(c1.get_all_missions())
    # print(c1.get_mission_by_id(3))
    print(c1.assign_mission(1,3))
    # print(c1.update_mission_status(3,"hhhniuh"))
    print(c1.get_open_missions_by_agent(3))
    # print(c1.count_all_missions())
    # print(c1.count_by_status("in_progress"))
    # print(c1.count_critical_missions())
    # print(c1.get_top_agent())

