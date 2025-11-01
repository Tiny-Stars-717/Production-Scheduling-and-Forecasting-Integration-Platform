import sqlite3
import os
import json
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'smart_factory.db')

SCHEMA_SQL = """
-- 配置表
CREATE TABLE IF NOT EXISTS config (
    key TEXT PRIMARY KEY,
    value TEXT
);

-- 历史记录表
CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    module TEXT NOT NULL,
    algorithm TEXT NOT NULL,
    params TEXT,
    result TEXT,
    timestamp TEXT NOT NULL
);

-- 排产订单表
CREATE TABLE IF NOT EXISTS orders (
    order_id TEXT PRIMARY KEY,
    due_date INTEGER NOT NULL,
    processing_time INTEGER NOT NULL
);

-- 生产需求表
CREATE TABLE IF NOT EXISTS demand (
    date TEXT PRIMARY KEY,
    demand INTEGER NOT NULL
);

-- 库存表
CREATE TABLE IF NOT EXISTS stock (
    date TEXT PRIMARY KEY,
    stock INTEGER NOT NULL
);
"""

DEMO_DATA = {
    "config": [
        ("last_path", "")
    ],
    "orders": [
        ("A001", 10, 3),
        ("A002", 8, 2),
        ("A003", 15, 5),
        ("A004", 12, 4),
        ("A005", 9, 1)
    ],
    "demand": [
        ("2025-10-20", 100),
        ("2025-10-21", 120),
        ("2025-10-22", 80),
        ("2025-10-23", 90),
        ("2025-10-24", 110)
    ],
    "stock": [
        ("2025-10-20", 50),
        ("2025-10-21", 60),
        ("2025-10-22", 40),
        ("2025-10-23", 45),
        ("2025-10-24", 55)
    ]
}

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 创建 schema
    cursor.executescript(SCHEMA_SQL)
    conn.commit()

    # 导入 demo 数据
    for table, rows in DEMO_DATA.items():
        if table == 'config':
            cursor.executemany("INSERT OR REPLACE INTO config (key, value) VALUES (?, ?)", rows)
        elif table == 'orders':
            cursor.executemany("INSERT OR REPLACE INTO orders (order_id, due_date, processing_time) VALUES (?, ?, ?)", rows)
        elif table == 'demand':
            cursor.executemany("INSERT OR REPLACE INTO demand (date, demand) VALUES (?, ?)", rows)
        elif table == 'stock':
            cursor.executemany("INSERT OR REPLACE INTO stock (date, stock) VALUES (?, ?)", rows)
    conn.commit()
    conn.close()
    print(f"[{datetime.now()}] Database initialized at {DB_PATH} with demo data.")

if __name__ == "__main__":
    init_db()
