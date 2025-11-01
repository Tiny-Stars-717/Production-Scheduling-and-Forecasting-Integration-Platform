from flask import Blueprint, request, jsonify
from backend.utils.history_utils import get_history, delete_record

history_bp = Blueprint('history_bp', __name__)

# 查询历史记录
@history_bp.route('/<module>', methods=['GET'])
def get_module_history(module):
    limit = int(request.args.get('limit', 20))
    start_time = request.args.get('startTime')
    end_time = request.args.get('endTime')
    history_list = get_history(module, limit, start_time, end_time)
    return jsonify({"status": "success", "historyList": history_list})

# 删除历史记录
@history_bp.route('/<module>', methods=['DELETE'])
def delete_module_record(module):
    record_id = request.json.get('recordId')
    if not record_id:
        return jsonify({"status": "fail", "msg": "recordId不能为空"})
    delete_record(module, record_id)
    return jsonify({"status": "success"})
