import mysql.connector

class DBconnection:
    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.password = "1234"
        self.database="Intelligence_db"
        self.create_database()
        self.create_tables()


    def get_connection(self):
        return mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database = self.database
            )
    def create_database(self):
        conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password
            )
        cursor = conn.cursor()
        sql = "CREATE DATABASE IF NOT EXISTS Intelligence_db "
        cursor.execute(sql)
        conn.commit()
        success= cursor.rowcount > 0
        conn.close()
        cursor.close()
        return success
    def create_tables(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        sql =(" CREATE TABLE IF NOT EXISTS agents(" \
        "id INT AUTO_INCREMENT PRIMARY KEY," \
        "name VARCHAR(50) NOT NULL," \
        "specialty VARCHAR(50) NOT NULL," \
        "is_active BOOLEAN DEFAULT TRUE," \
        "completed_missions INT DEFAULT 0," \
        "failed_missions INT DEFAULT 0," \
        "agent_rank ENUM('Junior','Senior','Commander'))",
        "CREATE TABLE IF NOT EXISTS missions(" \
        "id INT AUTO_INCREMENT PRIMARY KEY," \
        "title VARCHAR(50) NOT NULL,"
        "description TEXT NOT NULL,"
        "location VARCHAR(50) NOT NULL,"
        "difficulty INT NOT NULL,"
        "importance INT NOT NULL," \
        "status VARCHAR(50) DEFAULT 'new' NOT NULL,"
        "risk_level VARCHAR(50) NOT NULL,"
        "assigned_agent_id INT DEFAULT NULL)")
        for query in sql:
            cursor.execute(query)
        success= cursor.rowcount > 0
        conn.commit()
        conn.close()
        cursor.close()
        return success

        
    
if __name__ == "__main__":
    c1 = DBconnection()
    # print(c1.create_database())
    print(c1.create_tables())
    # print(c1)


        

