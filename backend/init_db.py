import pymysql
import time

# 数据库配置
DB_HOST = "mysql.tonaspace.com"
DB_PORT = 3306
DB_USER = "root"
DB_PASSWORD = "TONA1234"
DB_NAME = "react_flask_demo"

def init_database():
    # 连接到MySQL服务器
    conn = pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        charset='utf8mb4'
    )
    
    cursor = conn.cursor()
    
    try:
        # 创建数据库
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print(f"数据库 {DB_NAME} 创建成功或已存在")
        
        # 切换到新创建的数据库
        cursor.execute(f"USE {DB_NAME}")
        
        # 创建图表数据表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS chart_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            category VARCHAR(50) NOT NULL,
            value INT NOT NULL,
            chart_type VARCHAR(20) NOT NULL
        )
        """)
        print("表 chart_data 创建成功或已存在")
        
        # 检查是否有数据，如果没有则插入样例数据
        cursor.execute("SELECT COUNT(*) FROM chart_data")
        result = cursor.fetchone()
        count = result[0] if result else 0
        
        if count == 0:
            # 插入柱状图数据
            bar_data = [
                ('类别1', 120, 'bar'),
                ('类别2', 200, 'bar'),
                ('类别3', 150, 'bar'),
                ('类别4', 80, 'bar'),
                ('类别5', 70, 'bar')
            ]
            
            # 插入折线图数据
            line_data = [
                ('一月', 100, 'line'),
                ('二月', 120, 'line'),
                ('三月', 140, 'line'),
                ('四月', 160, 'line'),
                ('五月', 180, 'line')
            ]
            
            # 插入饼图数据
            pie_data = [
                ('产品A', 30, 'pie'),
                ('产品B', 40, 'pie'),
                ('产品C', 20, 'pie'),
                ('产品D', 10, 'pie')
            ]
            
            # 合并所有数据
            all_data = bar_data + line_data + pie_data
            
            # 批量插入数据
            cursor.executemany(
                "INSERT INTO chart_data (category, value, chart_type) VALUES (%s, %s, %s)",
                all_data
            )
            
            conn.commit()
            print(f"已插入 {len(all_data)} 条样例数据")
        else:
            print(f"表中已有 {count} 条数据，跳过插入样例数据")
        
        print("数据库初始化完成")
        
    except Exception as e:
        conn.rollback()
        print(f"初始化数据库出错: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    init_database() 