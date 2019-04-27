from flask import Blueprint,request,redirect,jsonify
from common.libs.Helper import ops_render
from common.models.User import User
from common.libs.UrlManager import UrlManager
from application import app,db
from sqlalchemy import or_

route_account = Blueprint('account_page',__name__)


@route_account.route('/index')
def index():
    resp_data = {}
    req = request.values
    query = User.query

    if 'mix_kw' in req:
        rule = or_(User.nickname.ilike("%{0}%".format(req['mix_kw'])))
        query = query.filter(rule)

    if 'status' in req and int(req['status'])>-1:
        query = query.filter(User.status==int(req['status']))

    list = query.order_by(User.status.desc(),User.uid.asc()).all()

    resp_data['list'] = list
    resp_data['search_con'] = req
    resp_data['status_mapping'] = app.config['STATUS_MAPPING']

    return ops_render('account/index.html', resp_data)


# 删除恢复
@route_account.route('/ops',methods=["POST"])
def ops():
    prompt = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values

    id = req['id'] if 'id' in req else ''
    act = req['act'] if 'act' in req else ''

    if not id:
        prompt['code'] = -1
        prompt['msg'] = "请选择要操作的账号！"
        return jsonify(prompt)

    if act not in ["remove","recover"]:
        prompt['code'] = -1
        prompt['msg'] = "操作有误！"
        return jsonify(prompt)

    user_info = User.query.filter_by(uid=id).first()
    if not user_info:
        prompt['code'] = -1
        prompt['msg'] = "账号不存在！"
        return jsonify(prompt)

    if user_info and user_info.uid == 1:
        prompt['code'] = -1
        prompt['msg'] = "最高权限账号不允许删除！"
        return jsonify(prompt)

    if act == "remove":
        user_info.status = 0
    elif act == "recover":
        user_info.status = 1

    db.session.add(user_info)
    db.session.commit()
    return jsonify(prompt)
