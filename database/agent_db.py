from database.db_connection import DBconnection
connection = DBconnection()

class AgentDB:
    def create_agent(self,data:dict):
        conn = connection.get_connection()
        cursor  = conn.cursor(dictionary=True)
        query = "INSERT INTO agents (name, specialty, agent_rank) VALUES (%s,%s,%s)"
        val =list(data.values())
        print(val)
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
    
if __name__ == "__main__":
    c1 =AgentDB()
    # c1.create_agent({"name":"avi","specialty":"hbdfhb","agent_rank":"Senior"})
    # print(c1.get_all_agents())
    # print(c1.get_agent_by_id(3))
    print(c1.update_agent(2,{"name":"moshe"}))

