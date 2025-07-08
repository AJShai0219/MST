from mysql_helper import MySQLHelper

def main():
    config = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': '123456',  
        'database': 't1',
        'charset': 'utf8'
    }

    
    helper = MySQLHelper(**config)  
    print("\n查询:")
    select_sql = "SELECT * FROM t1"
    users = helper.execute_query(select_sql)
    for user in users:
       print(user)
    
if __name__ == "__main__":
    print("1")
    main()    
