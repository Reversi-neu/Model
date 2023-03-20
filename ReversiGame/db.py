import pymysql

class DB:
    def __init__(self):
        self.conn = pymysql.connect(
            host= 'reversi-db.co96znypdwjk.us-east-2.rds.amazonaws.com', 
            port = 3306,
            user = 'admin', 
            password = 'e5YVS9D11OBvShYwu8gA',
            db = 'reversidb',       
        )
    
    def callDB(self, statement, data):
        cursor = self.conn.cursor()
        cursor.execute(statement, data)
        rv = cursor.fetchall()
        self.conn.commit()
        cursor.close()
        return rv