# _*_coding:utf-8_*_


from flask import jsonify
from .dbtools import DatabaseAgent
import re

MSG_MAP = {
    200: 'success',
    401: '未提供认证信息',
    402: '认证信息过期，请重新登录',
    403: '错误的认证信息',
    404: '请求内容不存在',
    405: '不允许的操作',
    410: '用户名已存在',
    421: '用户名或密码错误',
    422: '请求缺少必要参数',
    500: '请求错误，请联系管理员',
    501: 'JSON格式错误',
    10000: '目录名已存在',
    10001: '文件传输错误'
}

AREA_MAP = {
    "shanghai":"上海",
    "zhejiang":"浙江",
    "jiangsu":"江苏",
    "anhui":"安徽",
    "chanyelianmeng":"工业互联网产业联盟"
}

# 过滤html标签
def filter_tags(htmlstr):
    #先过滤CDATA
    re_cdata=re.compile('//<!\[CDATA\[[^>]*//\]\]>',re.I) #匹配CDATA
    re_script=re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)#Script
    re_style=re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>',re.I)#style
    re_br=re.compile('<br\s*?/?>')#处理换行
    re_h=re.compile('</?\w+[^>]*>')#HTML标签
    re_comment=re.compile('<!--[^>]*-->')#HTML注释
    # s=re_cdata.sub('',htmlstr)#去掉CDATA
    s=re_script.sub('',s) #去掉SCRIPT
    s=re_style.sub('',s)#去掉style
    s=re_br.sub('\n',s)#将br转换为换行
    s=re_h.sub('',s) #去掉HTML 标签
    s=re_comment.sub('',s)#去掉HTML注释
    #去掉多余的空行
    blank_line=re.compile('\n+')
    s=blank_line.sub('\n',s)
    s=replaceCharEntity(s)#替换实体
    return s


##替换常用HTML字符实体.
# 使用正常的字符替换HTML中特殊的字符实体.
# 你可以添加新的实体字符到CHAR_ENTITIES中,处理更多HTML字符实体.
# @param htmlstr HTML字符串.
def replaceCharEntity(htmlstr):
    CHAR_ENTITIES = {'nbsp': ' ', '160': ' ',
                     'lt': '<', '60': '<',
                     'gt': '>', '62': '>',
                     'amp': '&', '38': '&',
                     'quot': '"', '34': '"', }

    re_charEntity = re.compile(r'&#?(?P<name>\w+);')
    sz = re_charEntity.search(htmlstr)
    while sz:
        entity = sz.group()  # entity全称，如&gt;
        key = sz.group('name')  # 去除&;后entity,如&gt;为gt
        try:
            htmlstr = re_charEntity.sub(CHAR_ENTITIES[key], htmlstr, 1)
            sz = re_charEntity.search(htmlstr)
        except KeyError:
            # 以空串代替
            htmlstr = re_charEntity.sub('', htmlstr, 1)
            sz = re_charEntity.search(htmlstr)
    return htmlstr


# 验证请求是否完整
def params_inact(post_data, *args):
    if not isinstance(post_data, dict):
        return False
    for arg in args:
        if arg not in post_data.keys():
            print("miss {} filed ".format(arg))
            return False
    return True


# 统一格式返回
def to_json(code, data=None):
    return jsonify({
        "code": code,
        "msg": MSG_MAP[code],
        "data": data
    })


# 过滤垃圾字符
# def clear(data):
#     return data.strip().replace('\n', '').replace('\t', '').replace('\r', '').replace(',', '').replace('.',
#                                                                                                        '').replace(
#         '!', '').replace('，', '').replace('。', '').replace('！', '').replace('、', '').replace(':', '').replace('：',
#                                                                                                               '').replace(
#         ' ', '').replace('"', '').replace('\'', '').replace('“', '').replace('”', '').replace('；', '').replace('(',
#                                                                                                                '').replace(
#         ')', '')

# 数字文字分词存储
def parse_word(description, word_model):
    db_agent = DatabaseAgent()
    seg_list = jieba.cut(description)
    for x in seg_list:
        if x == " ":
            continue
        exists = db_agent.get(
            filter_kwargs={
                "word": str(x)
            },
            orm_model=word_model
        )
        if exists:
            db_agent.update(
                filter_kwargs={
                    "word": str(x)
                },
                method_kwargs={
                    "count": 1 + exists.count
                },
                orm_model=word_model
            )
        else:
            db_agent.add(
                kwargs={
                    "word": str(x),
                    "count": 1
                },
                orm_model=word_model
            )
