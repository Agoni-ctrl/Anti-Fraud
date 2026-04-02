@echo off
title AI反诈助手 - 后端服务
echo ========================================
echo    AI反诈助手 - Flask 后端服务
echo ========================================
echo.

cd /d D:\my project\Anti-Fraud

echo 正在激活虚拟环境...
call .venv\Scripts\activate

echo 正在设置 API Key...
set DASHSCOPE_API_KEY=sk-ba8e6bbaf3b64ff0839332fc37b88dc8

echo 正在启动服务...
echo.
echo 服务启动后，请保持此窗口打开
echo 按 Ctrl+C 可停止服务
echo ========================================
echo.

python api_server.py

pause