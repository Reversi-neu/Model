import pymysql

# DESIGN PATTERN: Singleton
class DB:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

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