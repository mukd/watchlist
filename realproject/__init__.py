import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from realproject.settings import BASE_DIR

app = Flask(__name__, instance_relative_config=True)
db = SQLAlchemy()

def create_app(test_config=None):

    if test_config is None:
        CONFIG_DIR = BASE_DIR / 'realproject/settings.py'
        app.config.from_pyfile(CONFIG_DIR,silent=True)
    else:
        app.config.from_mapping(test_config)
    #绑定数据库
    db.init_app(app)

    #注册migrate
    #递归创建目录，确保项目文件存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    # 注册视图
    register_bg(app)

    return app

def register_bg(app:Flask):
    """注册视图方法"""
    from app.watlist import views as watlist
    from app.watlist import models
    #注册蓝图
    app.register_blueprint(watlist.bg)

    #首页url
    #app.add_url_rule(rule='/',endpoint='index',view_func=watlist.hello.index)