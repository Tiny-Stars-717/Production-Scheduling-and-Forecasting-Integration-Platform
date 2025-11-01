from flask import Blueprint, request, jsonify
from backend.ml_models.stock_optimization import run_stock
from backend.utils.history_utils import save_history

plan_bp = Blueprint('plan_bp', __name__)

@plan_bp.route('/run', methods=['POST'])
def run():
    try:
        data = request.json
        print("📥 接收到库存优化请求：", data)

        algorithm = data.get('algorithm')  # 'lp' / 'pso'
        forecast_data = data.get('forecastData')

        if not forecast_data:
            return jsonify({"status": "fail", "msg": "输入数据为空或格式错误"}), 400

        stock_result, chart_data = run_stock(forecast_data, algorithm)

        # ✅ 保存历史记录
        save_history(
            module="stock",
            algorithm=algorithm,
            params={"forecastData": forecast_data},
            result={"stockResult": stock_result, "chartData": chart_data}
        )

        return jsonify({
            "status": "success",
            "stockResult": stock_result,
            "chartData": chart_data
        })

    except Exception as e:
        import traceback
        print("❌ 库存优化运行错误：", e)
        print(traceback.format_exc())
        return jsonify({"status": "error", "msg": str(e)}), 500
