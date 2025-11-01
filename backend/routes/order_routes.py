from flask import Blueprint, request, jsonify
import pandas as pd
from backend.utils.db_utils import save_last_path, get_last_path

order_bp = Blueprint('order_bp', __name__)

@order_bp.route('/upload', methods=['POST'])
def upload_excel():
    file = request.files.get('file')
    if not file:
        return jsonify({"status": "fail", "msg": "未上传文件"})
    try:
        # 不使用默认列名
        df = pd.read_excel(file, header=0)  # 第一行是列名
        df = df.fillna('')  # 空单元格填空字符串
        data = df.to_dict(orient='records')
        return jsonify({"status": "success", "data": data})
    except Exception as e:
        return jsonify({"status": "fail", "msg": str(e)})

@order_bp.route('/read', methods=['POST'])
def read_file():
    filepath = request.json.get('filepath')
    try:
        df = pd.read_excel(filepath, header=0)
        df = df.fillna('')
        save_last_path(filepath)
        return jsonify({"status": "success", "data": df.to_dict('records')})
    except Exception as e:
        return jsonify({"status": "fail", "msg": str(e)})

@order_bp.route('/get_path', methods=['GET'])
def get_path():
    path = get_last_path()
    return jsonify({"status": "success", "filepath": path})
