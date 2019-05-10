# -*- coding: utf-8 -*-
from flask import Blueprint,request,redirect,jsonify
from common.libs.Helper import ops_render
from common.models.Member import Member
from common.models.MemberAddress import MemberAddres
from common.models.PayOrder import PayOrder
from common.models.Food import Food
from common.libs.Helper import getDictList
from application import app,db
from sqlalchemy import or_
from common.libs.UrlManager import UrlManager


route_member = Blueprint( 'member_page',__name__ )


# 列表
@route_member.route( "/index" )
def index():
    resp_data = {}
    req = request.values
    query = Member.query

    if 'mix_kw' in req:
        rule = or_(Member.nickname.ilike("%{0}%".format(req['mix_kw'])))
        query = query.filter(rule)

    if 'status' in req and int(req['status'])>-1:
        query = query.filter(Member.status==int(req['status']))

    if 'purview' in req and int(req['purview'])>-1:
        query = query.filter(Member.purview==int(req['purview']))

    list = query.order_by(Member.status.desc(),Member.id.asc()).all()

    resp_data['list'] = list
    resp_data['search_con'] = req
    resp_data['status_mapping'] = app.config['STATUS_MAPPING']
    resp_data['purview_mapping'] = app.config['PURVIEW_MAPPING']

    resp_data['current'] = 'index'
    return ops_render( "member/index.html",resp_data )


# 详情
@route_member.route( "/info" )
def info():
    resp_data = {}
    req = request.args
    id = int(req.get('id', 0))

    if id < 1:
        return redirect(UrlManager.buildUrl("/member/index"))

    info = Member.query.filter_by(id=id).first()
    if not info:
        return redirect(UrlManager.buildUrl("/member/index"))
    address_info = MemberAddres.query.filter_by(member_id=id).first()

    ids = [id]
    pay_order_map = getDictList(PayOrder, PayOrder.member_id, "member_id", ids)
    pay_order_list = []
    if pay_order_map:
        pay_order_list = pay_order_map[id]

    food_map = getDictList(Food, Food.member_id, "member_id", ids)
    food_list = []
    if food_map:
        food_list = food_map[id]

    resp_data['search_con'] = req
    resp_data['info'] = info
    resp_data['pay_order_list'] = pay_order_list
    resp_data['food_list'] = food_list
    resp_data['address_info'] = address_info
    resp_data['current'] = 'index'

    return ops_render( "member/info.html",resp_data )


# 删除恢复
@route_member.route('/ops',methods=["POST"])
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

    member_info = Member.query.filter_by(id=id).first()
    if not member_info:
        prompt['code'] = -1
        prompt['msg'] = "账号不存在！"
        return jsonify(prompt)

    if act == "remove":
        member_info.status = 0
    elif act == "recover":
        member_info.status = 1

    if member_info.status == 0:
        ids = [id]
        food_map = getDictList(Food, Food.member_id, "member_id", ids)
        food_list = food_map[member_info.id]
        for item in food_list:
            item.status = 0

    db.session.add(member_info)
    db.session.commit()
    return jsonify(prompt)


@route_member.route('/ok',methods=["POST"])
def ok():
    prompt = {'code': 200, 'msg': '审核通过', 'data': {}}
    req = request.values

    id = req['id'] if 'id' in req else ''

    member_info = Member.query.filter_by(id=id).first()

    member_info.purview = 0

    db.session.add(member_info)
    db.session.commit()
    return jsonify(prompt)



