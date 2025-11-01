import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 数据库配置
DATABASE = os.path.join(BASE_DIR, '../database/smart_factory.db')

# 日志配置
LOG_DIR = os.path.join(BASE_DIR, 'logs')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
LOG_FILE = os.path.join(LOG_DIR, 'app.log')

# Flask配置
DEBUG = False
SECRET_KEY = 'smart_factory_secret_key'
