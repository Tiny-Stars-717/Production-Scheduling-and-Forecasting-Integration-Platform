# backend/app.py
from flask import Flask
from flask_cors import CORS

# 导入蓝图（各功能模块）
from backend.routes.order_routes import order_bp
from backend.routes.predict_routes import predict_bp
from backend.routes.schedule_routes import schedule_bp
from backend.routes.plan_routes import plan_bp
from backend.routes.history_routes import history_bp


def create_app():
    """创建并配置 Flask 应用"""
    app = Flask(__name__)
    CORS(app)  # 允许跨域请求（前后端联调必须）

    # 注册蓝图（后端模块）
    app.register_blueprint(order_bp, url_prefix='/api/order')
    app.register_blueprint(schedule_bp, url_prefix='/api/schedule')
    app.register_blueprint(predict_bp, url_prefix='/api/forecast')
    app.register_blueprint(plan_bp, url_prefix='/api/stock')
    app.register_blueprint(history_bp, url_prefix='/api/history')

    return app


# 程序入口
if __name__ == "__main__":
    app = create_app()
    # 绑定 0.0.0.0，外部可访问，调试时开启 debug 模式方便定位问题
    app.run(host='0.0.0.0', port=5000, debug=True)
