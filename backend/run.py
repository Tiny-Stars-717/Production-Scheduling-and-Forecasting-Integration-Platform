# Flask 启动入口

from backend.app import create_app

# 创建 Flask 应用
app = create_app()

if __name__ == "__main__":
    # 启动服务
    app.run(host="0.0.0.0", port=5000, debug=True)
