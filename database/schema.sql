-- ==========================
-- 配置表：保存最近导入路径等
-- ==========================
CREATE TABLE IF NOT EXISTS config (
    key TEXT PRIMARY KEY,
    value TEXT
);

-- ==========================
-- 历史记录表
-- ==========================
CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    module TEXT NOT NULL,       -- schedule / forecast / stock
    algorithm TEXT NOT NULL,    -- 使用的算法
    params TEXT,                -- JSON 存储输入参数
    result TEXT,                -- JSON 存储输出结果
    timestamp TEXT NOT NULL     -- 操作时间
);

-- ==========================
-- 可扩展生产数据表（可选）
-- ==========================
CREATE TABLE IF NOT EXISTS orders (
    order_id TEXT PRIMARY KEY,
    due_date INTEGER NOT NULL,
    processing_time INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS demand (
    date TEXT PRIMARY KEY,
    demand INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS stock (
    date TEXT PRIMARY KEY,
    stock INTEGER NOT NULL
);
