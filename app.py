# __coding:utf-8__
'''
@Author  : Sun
@Time    :  上午11:01
@Software: PyCharm
@File    : app.py.py
'''


from flask_script import Manager, Server
from flask_app import create_app
import os

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)


@app.route('/')
def hello():
    return 'hello'


if __name__ == '__main__':
    manager.add_command("runserver",
                        Server(host="0.0.0.0", port=10011, threaded=True))
    manager.run()
