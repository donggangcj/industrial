# __coding:utf-8__
'''
@Author  : Sun
@Time    :  上午11:05
@Software: PyCharm
@File    : __init__.py
'''

from flask_cors import *
from flask import Flask

def create_app(config_name):
    app = Flask(__name__)
    CORS(app, supports_credentials=True)

    from route.index import api
    app.register_blueprint(api, url_prefix='/industrial')

    return app