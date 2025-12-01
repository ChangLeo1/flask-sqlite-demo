from flask import Flask
from .routes import bp

def create_app():
    app = Flask(__name__)

    # 注册蓝图
    app.register_blueprint(bp)

    # teardown 时关闭数据库连接
    from .db import close_db
    app.teardown_appcontext(close_db)

    return app
