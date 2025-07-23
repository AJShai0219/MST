from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
import os

app = Flask(__name__)
CORS(app)  # 启用CORS

# 数据库配置
DB_HOST = "mysql.tonaspace.com"
DB_PORT = 3306
DB_USER = "root"
DB_PASSWORD = "TONA1234"
DB_NAME = "react_flask_demo"

# 连接到MySQL数据库
def get_db_connection():
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            charset='utf8mb4'
        )
        return connection
    except Exception as e:
        print(f"数据库连接错误: {e}")
        return None

# GET请求接口
@app.route('/api/get-data', methods=['GET'])
def get_data():
    input_value = request.args.get('input_value', '')
    response = {
        "status": 200,
        "message": "成功",
        "data": f"您输入的参数是：{input_value}"
    }
    return jsonify(response)

# POST请求接口
@app.route('/api/post-data', methods=['POST'])
def post_data():
    data = request.json
    body_value = data.get('body_value', '') if data else ''
    param_value = request.args.get('param_value', '')
    
    response = {
        "status": 200,
        "message": "成功",
        "data": {
            "body": f"接收到的body参数是：{body_value}",
            "param": f"接收到的param参数是：{param_value}"
        }
    }
    return jsonify(response)

# 图表数据接口
@app.route('/api/chart-data', methods=['GET'])
def chart_data():
    chart_type = request.args.get('chart_type', 'bar')
    
    try:
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            # 查询特定图表类型的数据
            sql = "SELECT category, value FROM chart_data WHERE chart_type = %s"
            cursor.execute(sql, (chart_type,))
            result = cursor.fetchall()
            
            # 获取列名
            field_names = [i[0] for i in cursor.description]
            
            # 构建数据结构
            categories = []
            values = []
            
            # 遍历结果，第0列是category，第1列是value
            for row in result:
                categories.append(row[0])  # category
                values.append(row[1])      # value
            
            cursor.close()
            connection.close()
            
            response = {
                "status": 200,
                "message": "成功",
                "data": {
                    "xAxis": categories,
                    "series": values,
                    "chartType": chart_type
                }
            }
        else:
            response = {
                "status": 500,
                "message": "数据库连接失败",
                "data": None
            }
    except Exception as e:
        print(f"查询数据错误: {e}")
        response = {
            "status": 500,
            "message": f"错误: {str(e)}",
            "data": None
        }
    
    return jsonify(response)

# 启动应用
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 