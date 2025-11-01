from backend.utils.db_utils import execute_query
from datetime import datetime
import json


def save_history(module, algorithm, params, result):
    """
    保存操作历史记录
    :param module: 模块名，如 "schedule"、"forecast"、"stock"
    :param algorithm: 使用的算法名称，如 "EDD"、"ARIMA"、"PSO"
    :param params: 输入参数（通常为前端传入的原始数据）
    :param result: 计算结果（算法输出结果）
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 确保数据可序列化
    params_json = json.dumps(params, ensure_ascii=False)
    result_json = json.dumps(result, ensure_ascii=False)

    execute_query(
        """
        INSERT INTO history (module, algorithm, params, result, timestamp)
        VALUES (?, ?, ?, ?, ?)
        """,
        (module, algorithm, params_json, result_json, timestamp)
    )

    print(f"✅ 已保存历史记录: 模块={module}, 算法={algorithm}, 时间={timestamp}")


def get_history(module, limit=20, start_time=None, end_time=None):
    """
    获取历史记录，可按时间筛选
    """
    query = """
        SELECT id, module, algorithm, params, result, timestamp
        FROM history
        WHERE module=?
    """
    params = [module]

    if start_time and end_time:
        query += " AND timestamp BETWEEN ? AND ?"
        params.extend([start_time, end_time])

    query += " ORDER BY timestamp DESC LIMIT ?"
    params.append(limit)

    rows = execute_query(query, params, fetch=True)

    history_list = []
    for row in rows:
        history_list.append({
            "recordId": row[0],
            "module": row[1],
            "algorithm": row[2],
            "params": json.loads(row[3]),
            "result": json.loads(row[4]),
            "timestamp": row[5]
        })

    return history_list


def delete_record(module, record_id):
    """
    删除指定历史记录
    """
    execute_query(
        "DELETE FROM history WHERE module=? AND id=?",
        (module, record_id)
    )

    print(f"🗑️ 已删除记录: 模块={module}, ID={record_id}")
