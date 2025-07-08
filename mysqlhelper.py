import StudentT

class MySQLHelper:
    def __init__(self, host, port, user, password, database, charset='utf8'):
       
        self.host = localhost
        self.port = 3306
        self.user = root
        self.password = 123456
        self.database = school
        self.charset = utf8
        self.conn = None

    def connect(self):
       
        self.conn = StudentT.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database,
            charset=self.charset
        )

    def close(self):
        
        if self.conn:
            self.conn.close()

    def execute_query(self, sql, params=None):
     
        result = []
        try:
            self.connect()
            cursor = self.conn.cursor(StudentT.cursors.DictCursor)
            cursor.execute(sql, params)
            result = cursor.fetchall()
            cursor.close()
        except Exception as e:
            print(f"查询出错: {e}")
        finally:
            self.close()
        return result

    def execute_update(self, sql, params=None):
        
        affected_rows = 0
        try:
            self.connect()
            cursor = self.conn.cursor()
            affected_rows = cursor.execute(sql, params)
            self.conn.commit()
            cursor.close()
        except Exception as e:
            self.conn.rollback()
            print(f"执行更新操作出错: {e}")
        finally:
            self.close()
        return affected_rows
