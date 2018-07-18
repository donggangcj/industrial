# __coding:utf-8__
'''
@Author  : Sun
@Time    :  上午11:06
@Software: PyCharm
@File    : index.py
'''


import time
from common.dbtools import DatabaseAgent, sqlalchemy_session
from common.common import to_json
from flask import request, Blueprint
from job.models.industrial import Industrial

api = Blueprint('api', __name__)

@api.route("/latest", methods=['get'])
def get_latest():
    res = []
    with sqlalchemy_session() as session:
        latest_new = session.query(Industrial).order_by("time").limit(10).all()
        for new in latest_new:
            res.append({"id":new.id,"title":new.title,"time":new.time,"url":new.url,"area":new.area,"nature":new.nature})
        return to_json(200, res)

@api.route("/news", methods=['post','get'])
def get_news():
    res = []
    data = request.json
    date = data.get("time",0)
    if date == 0:
        date = [0,time.time()]
    with sqlalchemy_session() as session:
        if data:
            count = session.query(Industrial).filter((Industrial.time >= date[0]) & (date[1] >= Industrial.time)).filter_by(**{"area":data["area"]}).count()
            news = session.query(Industrial).filter((Industrial.time >= date[0]) & (date[1] >= Industrial.time)).filter_by(**{"area":data["area"]}).order_by("time").limit(10).offset((data["page"])*10)
        else:
            news = session.query(Industrial).filter((Industrial.time >= date[0]) & (date[1] >= Industrial.time)).order_by("time").limit(10).offset((data["page"])*10)

        for new in news:
            res.append({"id":new.id,"title":new.title,"time":new.time,"url":new.url,"area":new.area,"nature":new.nature})
        return to_json(200, {"items":res,"page":int(count / 10) + 1})
