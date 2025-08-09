from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
import os
from werkzeug.security import generate_password_hash, check_password_hash
from PIL import Image
import torch
import torchvision.transforms as transforms

from minist import Net, device

app = Flask(__name__)
CORS(app)  # 启用CORS

# 数据库配置
DB_HOST = "127.0.0.1"
DB_PORT = 3306
DB_USER = "root"
DB_PASSWORD = "root"
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
                values.append(row[1])  # value

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


# 注册接口
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    confirm = data.get('confirm')

    # 校验字段是否为空
    if not username or not password or not confirm:
        return jsonify({
            "status": 400,
            "message": "用户名、密码、确认密码不能为空",
            "data": None
        })

    # 校验两次密码是否一致
    if password != confirm:
        return jsonify({
            "status": 400,
            "message": "两次密码输入不一致",
            "data": None
        })

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # 检查用户名是否存在
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            return jsonify({
                "status": 409,
                "message": "用户名已存在",
                "data": None
            })

        # 密码加密
        hashed_password = generate_password_hash(password)
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({
            "status": 200,
            "message": "注册成功",
            "data": None
        })

    except Exception as e:
        print(f"注册错误: {e}")
        return jsonify({
            "status": 500,
            "message": "服务器内部错误",
            "data": None
        })


# 登录接口
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"status": 400, "message": "用户名和密码不能为空", "data": None})

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        cursor.close()
        connection.close()

        if user and check_password_hash(user[2], password):  # user[2] 是 password 字段
            return jsonify({"status": 200, "message": "登录成功", "data": {"username": username}})
        else:
            return jsonify({"status": 401, "message": "用户名或密码错误", "data": None})
    except Exception as e:
        print(f"登录错误: {e}")
        return jsonify({"status": 500, "message": "服务器内部错误", "data": None})


transform = transforms.Compose([
    transforms.Grayscale(num_output_channels=1),
    transforms.Resize((28, 28)),
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,))  # MNIST标准归一化
])

# 加载模型
model = Net()
model.load_state_dict(torch.load("mnist_model.pth", map_location=device))
model.to(device)
model.eval()


@app.route('/api/predict-digit', methods=['POST'])
def predict_digit():
    if 'file' not in request.files:
        return jsonify({"message": "没有上传文件", "result": None}), 400
    file = request.files['file']

    try:
        img = Image.open(file.stream)
        img_tensor = transform(img).view(-1, 28 * 28).to(device)  # 展平成1x784张量

        with torch.no_grad():
            output = model(img_tensor)
            pred = torch.argmax(output, dim=1).item()

        return jsonify({"message": "预测成功", "result": pred})

    except Exception as e:
        return jsonify({"message": f"预测出错: {str(e)}", "result": None}), 500


# 启动应用
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
