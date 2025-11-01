# 文件名: gunicorn_config.py
# 功能: Gunicorn 配置文件，适用于 Flask 生产环境

import multiprocessing
import os

# --------------------------
# 基本配置
# --------------------------
bind = "0.0.0.0:5000"  # 监听所有接口的5000端口
workers = multiprocessing.cpu_count() * 2 + 1  # 根据CPU核心数自动分配worker
threads = 2  # 每个worker使用2个线程
timeout = 120  # 请求超时时间（秒）
keepalive = 5  # 长连接保持时间（秒）

# --------------------------
# 日志配置
# --------------------------
loglevel = "info"
errorlog = "/app/backend/logs/gunicorn_error.log"  # 错误日志
accesslog = "/app/backend/logs/gunicorn_access.log"  # 访问日志
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# --------------------------
# 其他可选配置
# --------------------------
proc_name = "smart_factory_gunicorn"  # 进程名称
