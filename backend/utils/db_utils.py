import sqlite3
from backend.config import DATABASE

def execute_query(query, params=(), fetch=False):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(query, params)
    if fetch:
        result = cursor.fetchall()
    else:
        result = None
    conn.commit()
    cursor.close()
    conn.close()
    return result

# 保存最近导入路径
def save_last_path(filepath):
    execute_query(
        "INSERT OR REPLACE INTO config (key, value) VALUES (?, ?)",
        ("last_path", filepath)
    )

# 获取最近导入路径
def get_last_path():
    result = execute_query(
        "SELECT value FROM config WHERE key=?",
        ("last_path",),
        fetch=True
    )
    return result[0][0] if result else ""
