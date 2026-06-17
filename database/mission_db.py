from database.db_connection import DBconnection
connection = DBconnection()
 
class MissionDB:
    def create_mission(self,data:dict):
        conn = connection.get_connection()
        cursor  = conn.cursor(dictionary=True)
        if 1 > data["difficulty"] >10 and 1 > data["importance"] >10:
            raise ValueError ("please enter number between 1-10 only")
        level_risk = self.risk_level(data)
        print(level_risk)
        query = "INSERT INTO missions (title, description, location,difficulty,importance,risk_level) VALUES (%s,%s,%s,%s,%s,%s)"
        val =list(data.values())+[level_risk]
        print(val)
        cursor.execute(query,(val))
        conn.commit()
        agent = cursor.fetchone()
        conn.close()
        cursor.close()
        return agent
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
if __name__ == "__main__":
    c1 = MissionDB()
    # print(c1.create_mission({"title":"ydeg","description":'ghg','location':'ggg','difficulty':9,'importance':9}))
    # print(c1.get_all_missions())
    print(c1.get_mission_by_id(3))

