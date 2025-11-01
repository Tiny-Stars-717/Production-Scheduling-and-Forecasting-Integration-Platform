from flask import Blueprint, request, jsonify
from backend.ml_models.scheduling import run_schedule
from backend.utils.history_utils import save_history

schedule_bp = Blueprint('schedule_bp', __name__)

@schedule_bp.route('/run', methods=['POST'])
def run():
    try:
        data = request.json
        print("接收到前端数据：", data)

        algorithm = data.get('algorithm')
        input_data = data.get('inputData')

        if not input_data or not isinstance(input_data, list):
            return jsonify({"status": "fail", "msg": "输入数据为空或格式错误"}), 400

        # 运行调度算法
        schedule_result, metrics = run_schedule(input_data, algorithm)

        # 打印调试信息
        print(f"排产结果 ({len(schedule_result)} 条):")
        for r in schedule_result[:5]:  # 前5条示例
            print(r)
        print("性能指标:", metrics)

        # 保存历史
        save_history(
            module="schedule",
            algorithm=algorithm,
            params={"inputData": input_data},
            result={"result": schedule_result, "metrics": metrics}
        )

        # 确保每条记录都是 dict 类型（防止序列化错误）
        schedule_result = [dict(r) if not isinstance(r, dict) else r for r in schedule_result]

        return jsonify({
            "status": "success",
            "scheduleResult": schedule_result,
            "metrics": metrics
        })

    except Exception as e:
        import traceback
        print("调度运行错误：", e)
        print(traceback.format_exc())
        return jsonify({"status": "error", "msg": str(e)}), 500
