import pymysql
from werkzeug.security import generate_password_hash

# 数据库配置
DB_HOST = "127.0.0.1"
DB_PORT = 3306
DB_USER = "root"
DB_PASSWORD = "root"
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
        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS {DB_NAME} DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
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

        # 创建用户表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        print("表 users 创建成功或已存在")

        # 插入图表数据（如无）
        cursor.execute("SELECT COUNT(*) FROM chart_data")
        count_chart = cursor.fetchone()[0]

        if count_chart == 0:
            bar_data = [
                ('类别1', 120, 'bar'),
                ('类别2', 200, 'bar'),
                ('类别3', 150, 'bar'),
                ('类别4', 80, 'bar'),
                ('类别5', 70, 'bar')
            ]
            line_data = [
                ('一月', 100, 'line'),
                ('二月', 120, 'line'),
                ('三月', 140, 'line'),
                ('四月', 160, 'line'),
                ('五月', 180, 'line')
            ]
            pie_data = [
                ('产品A', 30, 'pie'),
                ('产品B', 40, 'pie'),
                ('产品C', 20, 'pie'),
                ('产品D', 10, 'pie')
            ]
            all_data = bar_data + line_data + pie_data
            cursor.executemany(
                "INSERT INTO chart_data (category, value, chart_type) VALUES (%s, %s, %s)",
                all_data
            )
            print(f"已插入 {len(all_data)} 条样例数据到 chart_data 表")
        else:
            print(f"chart_data 表已有 {count_chart} 条数据，跳过插入")

        # 插入默认管理员账户（如不存在）
        cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'admin'")
        admin_count = cursor.fetchone()[0]

        if admin_count == 0:
            hashed_password = generate_password_hash("admin")
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (%s, %s)",
                ('admin', hashed_password)
            )
            print("已创建管理员账号：admin / admin（密码已加密）")
        else:
            print("管理员账号已存在，跳过创建")

        conn.commit()
        print("数据库初始化完成")

    except Exception as e:
        conn.rollback()
        print(f"初始化数据库出错: {e}")
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    init_database()
