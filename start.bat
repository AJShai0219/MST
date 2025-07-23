@echo off
echo 启动前后端交互系统...
echo 1. 初始化数据库...
cd backend
python init_db.py

echo 2. 启动后端服务器...
start cmd /k "cd backend && python app.py"

echo 3. 启动前端开发服务器...
start cmd /k "cd frontend && npm start"

echo 系统启动完成!
echo 前端地址: http://localhost:3000
echo 后端地址: http://localhost:5000 