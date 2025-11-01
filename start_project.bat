@echo off
REM 一键启动 Flask + React + 数据库开发环境
REM -------- 设置命令行为 UTF-8，避免中文乱码 --------
chcp 65001 >nul
REM -------- 激活 Python 虚拟环境 --------
echo [INFO] 激活虚拟环境...
CALL "D:\app\anaconda\anaconda\Scripts\activate.bat" ceshi
IF ERRORLEVEL 1 (
    echo [ERROR] 激活虚拟环境失败，请检查路径
    pause
    exit /b
)

REM -------- 确保在 project_root 目录 --------
SET ROOT_DIR=%~dp0
cd /d %ROOT_DIR%

REM -------- 启动 Flask 后端 --------
echo [INFO] 启动后端 Flask...
cd project_root
start cmd /k "python -m backend.run"
cd ..

REM -------- 启动前端 React --------
echo [INFO] 启动前端 React...
start cmd /k "cd /d %ROOT_DIR%frontend && npm run dev"
cd ..

REM -------- 打开浏览器访问前端 --------
echo [INFO] 打开浏览器访问前端首页...
start http://localhost:5173

echo [INFO] 所有服务已启动
pause
