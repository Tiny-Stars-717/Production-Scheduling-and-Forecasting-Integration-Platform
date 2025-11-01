from flask import Blueprint, request, jsonify
from backend.ml_models.stock_optimization import optimize_stock_lp, optimize_stock_pso
from backend.utils.db_utils import add_history

stock_bp = Blueprint("stock_bp", __name__)

@stock_bp.route("/optimize", methods=["POST"])
def stock_optimize():
    data = request.json
    method = data.get("method", "LP")
    forecast_data = data.get("forecast_data", [])

    if method == "LP":
        optimized = optimize_stock_lp(forecast_data)
    elif method == "PSO":
        optimized = optimize_stock_pso(forecast_data)
    else:
        return jsonify({"status":"fail","message":"优化方法不存在"})

    add_history("stock", {"method": method}, {"optimized_count": len(optimized)})
    return jsonify({"status":"success","method":method,"optimized_stock":optimized})
