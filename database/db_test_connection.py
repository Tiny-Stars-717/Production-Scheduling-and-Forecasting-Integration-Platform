import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "smart_factory.db")

def test_connection():
    """测试数据库连接"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [t[0] for t in cur.fetchall()]
        print("✅ 数据库连接成功！当前表：", tables)
    except Exception as e:
        print("❌ 数据库连接失败：", e)
    finally:
        conn.close()

if __name__ == "__main__":
    test_connection()
