from database.db_connection import DBconnection
connection = DBconnection()

class AgentDB:
    def create_agent(self,data:dict):
        conn = connection.get_connection()
        cursor  = conn.cursor(dictionary=True)
        query = "INSERT INTO agents (name, specialty, agent_rank) VALUES (%s,%s,%s)"
        val =list(data.values())
        cursor.execute(query,(val))
        conn.commit()
        agent = cursor.fetchone()
        conn.close()
        cursor.close()
        return agent
    def get_all_agents(self):
        conn = connection.get_connection()
        cursor  = conn.cursor(dictionary=True)
        query = "SELECT * FROM agents"
        cursor.execute(query)
        all_agents = cursor.fetchall()
        conn.close()
        cursor.close()
        return all_agents
    def get_agent_by_id(self,id:int):
        conn = connection.get_connection()
        cursor  = conn.cursor(dictionary=True)
        query = "SELECT * FROM agents WHERE id = %s"
        cursor.execute(query,(id,))
        agent = cursor.fetchone()
        conn.close()
        cursor.close()
        if not agent:
            return None
        return agent
    def update_agent(self,id:int, data:dict):
        if not self.get_agent_by_id(id):
            raise ValueError("id not found")
        conn = connection.get_connection()
        cursor  = conn.cursor(dictionary=True)
        set_parts = []
        for key in data.keys():
            set_parts.append(key)
        set_query = ", ".join(set_parts)
        query = f"UPDATE agents SET {set_query} = %s WHERE id = %s"
        val = list(data.values()) + [id]
        cursor.execute(query,val)
        conn.commit()
        changed = cursor.rowcount > 0
        conn.close()
        cursor.close()
        return changed
    def deactivate_agent(self,id:int):
        if not self.get_agent_by_id(id):
            raise ValueError("id not found")
        conn = connection.get_connection()
        cursor  = conn.cursor(dictionary=True)
        query = "UPDATE agents SET is_active = FALSE WHERE id = %s"
        cursor.execute(query,(id,))
        conn.commit()
        changed = cursor.rowcount > 0
        conn.close()
        cursor.close()
        return changed
    def increment_completed(self,id:int):
        if not self.get_agent_by_id(id):
            raise ValueError("id not found")
        if not self.get_agent_by_id(id)["is_active"]:
            raise ValueError("the agent not active")
        conn = connection.get_connection()
        cursor  = conn.cursor(dictionary=True)
        increment = self.get_agent_by_id(id)["completed_missions"] + 1
        query = "UPDATE agents SET completed_missions = %s WHERE id = %s"
        val = [increment] + [id]
        cursor.execute(query,val)
        conn.commit()
        changed = cursor.rowcount > 0
        conn.close()
        cursor.close()
        return changed
    def increment_failed(self,id:int):
        if not self.get_agent_by_id(id):
            raise ValueError("id not found")
        if not self.get_agent_by_id(id)["is_active"]:
            raise ValueError("the agent not active")
        conn = connection.get_connection()
        cursor  = conn.cursor(dictionary=True)
        increment = self.get_agent_by_id(id)["failed_missions"] + 1
        query = "UPDATE agents SET failed_missions = %s WHERE id = %s"
        val = [increment] + [id]
        cursor.execute(query,val)
        conn.commit()
        changed = cursor.rowcount > 0
        conn.close()
        cursor.close()
        return changed
    def get_agent_performance(self,id:int):
        if not self.get_agent_by_id(id):
            raise ValueError("id not found")
        conn = connection.get_connection()
        cursor  = conn.cursor(dictionary=True)
        completed = self.get_agent_by_id(id)["completed_missions"]
        failed = self.get_agent_by_id(id)["failed_missions"]
        total = completed + failed
        success_rate = (completed / total) * 100
        return {"completed":completed,
                "failed":failed,
                "total":total,
                "success_rate":success_rate
                }
        

        
if __name__ == "__main__":
    c1 =AgentDB()
    # print(c1.create_agent({"name":"avi","specialty":"hbdfhb","agent_rank":"Senior"}))
    # print(c1.get_all_agents())
    # print(c1.get_agent_by_id(3))
    # print(c1.update_agent(3,{"name":"moshe"}))
    # print(c1.deactivate_agent(1))
    # print(c1.increment_completed(3))
    print(c1.increment_failed(1))
    # print(c1.get_agent_performance(3))

