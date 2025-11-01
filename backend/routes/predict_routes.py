from flask import Blueprint, request, jsonify
from backend.ml_models.demand_forecast import run_forecast
from backend.utils.history_utils import save_history

predict_bp = Blueprint('predict_bp', __name__)

@predict_bp.route('/run', methods=['POST'])
def run():
    try:
        data = request.json
        print("📥 接收到预测请求：", data)

        algorithm = data.get('algorithm')  # 'arima', 'exp_smooth'
        input_data = data.get('inputData')

        if not input_data:
            return jsonify({"status": "fail", "msg": "输入数据为空或格式错误"}), 400

        # ✅ 调用模型预测
        forecast_result, chart_data, _ = run_forecast(input_data, algorithm)

        # ✅ 保存历史记录（确保所有数值都是 Python 原生类型）
        save_history(
            module="forecast",
            algorithm=algorithm,
            params={"inputData": input_data},
            result={
                "forecastResult": forecast_result,
                "chartData": chart_data
            }
        )

        return jsonify({
            "status": "success",
            "forecastResult": forecast_result,
            "chartData": chart_data
        })

    except Exception as e:
        import traceback
        print("❌ 预测运行错误：", e)
        print(traceback.format_exc())
        return jsonify({"status": "error", "msg": str(e)}), 500
