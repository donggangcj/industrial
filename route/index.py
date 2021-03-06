# __coding:utf-8__
'''
@Author  : Sun
@Time    :  上午11:06
@Software: PyCharm
@File    : index.py
'''


import time
from common.dbtools import DatabaseAgent, sqlalchemy_session
from common.common import to_json, AREA_MAP, KEYWORD
from flask import request, Blueprint
from job.models.industrial import Industrial

api = Blueprint('api', __name__)

@api.route("/latest", methods=['post','get'])
def get_latest():
    res = []
    if request.method == "GET":
        page = 0
    else:
        data = request.json
        page = data["page"] if data.get("page",None) != None else 0
    now_time = time.time()
    last_time = now_time-604800
    with sqlalchemy_session() as session:
        count = session.query(Industrial).filter((Industrial.time >= last_time) & (now_time >= Industrial.time)).filter(Industrial.keyword.in_(data.get("key",["工业互联网","工业App","航天云网","根云","用友工业互联网","beacon","isesol"]))).count()
        latest_new = session.query(Industrial).filter((Industrial.time >= last_time) & (now_time >= Industrial.time)).filter(Industrial.keyword.in_(data.get("key",["工业互联网","工业App","航天云网","根云","用友工业互联网","beacon","isesol"]))).order_by(Industrial.time.desc()).limit(10).offset((int(page)) * 10)
        coun = 0
        for new in latest_new:
            coun += 1
            res.append({"id":new.id,"title":new.title,"time":new.time,"url":new.url,"area":AREA_MAP.get(new.area,None),"nature":new.nature,"keyword":new.keyword})
        return to_json(200, {"items":res,"page":int(count / 10) + 1})

@api.route("/news", methods=['post','get'])
def get_news():
    res = []
    data = request.json
    date = data.get("time",0)
    if date == 0:
        date = [0,2175696000]
    with sqlalchemy_session() as session:
        if data.get("area",None):
            count = session.query(Industrial).filter((Industrial.time >= date[0]) & (date[1] >= Industrial.time)).filter(Industrial.area.in_(data.get("area"))).filter(Industrial.keyword.in_(data.get("key",KEYWORD))).count()
            news = session.query(Industrial).filter((Industrial.time >= date[0]) & (date[1] >= Industrial.time)).filter(Industrial.area.in_(data.get("area"))).filter(Industrial.keyword.in_(data.get("key",KEYWORD))).order_by(Industrial.time.desc()).limit(10).offset((data["page"])*10)
        else:
            count = session.query(Industrial).filter((Industrial.time >= date[0]) & (date[1] >= Industrial.time)).filter(Industrial.keyword.in_(data.get("key",KEYWORD))).count()
            news = session.query(Industrial).filter((Industrial.time >= date[0]) & (date[1] >= Industrial.time)).filter(Industrial.keyword.in_(data.get("key",KEYWORD))).order_by(Industrial.time.desc()).limit(10).offset((data["page"])*10)

        for new in news:
            if new.keyword in data.get("key",[]) or data.get("key",None)==None:
                res.append({"id":new.id,"title":new.title,"time":new.time,"url":new.url,"area":AREA_MAP.get(new.area,None),"nature":new.nature,"keyword":new.keyword})
            else:
                continue
        return to_json(200, {"items":res,"page":int(count / 10) + 1})


