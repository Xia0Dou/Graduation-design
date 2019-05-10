# -*- coding: utf-8 -*-
from flask import Blueprint,request,redirect,jsonify
from common.libs.Helper import ops_render,getDict,getDictList,selectFilter
from common.models.MemberAddress import MemberAddres
from common.models.Member import Member
from common.models.Food import Food
from common.models.PayOrderItem import PayOrderItem
from common.models.PayOrder import PayOrder
from sqlalchemy import func
import json
from application import app,db
from common.libs.UrlManager import UrlManager

route_finance = Blueprint( 'finance_page',__name__ )


@route_finance.route( "/index" )
def index():
    resp_data = {}
    req = request.values
    query = PayOrder.query

    if 'status' in req and int(req['status']) > -1:
        query = query.filter(PayOrder.status == int(req['status']))

    pay_list = query.order_by(PayOrder.id.asc()).all()
    data_list = dataList(pay_list)

    resp_data['list'] = data_list
    resp_data['search_con'] = req
    resp_data['pay_status_mapping'] = app.config['PAY_STATUS_MAPPING']
    resp_data['current'] = 'index'

    return ops_render( "finance/index.html", resp_data)


@route_finance.route( "/pay-info" )
def payInfo():
    resp_data = {}
    req = request.args
    id = int(req.get('id', 0))

    if id < 1:
        return redirect(UrlManager.buildUrl("/finance/index"))

    pay_info = PayOrder.query.filter_by(id=id).first()
    member_info = Member.query.filter_by(id=pay_info.member_id).first()
    pay_item_info = PayOrderItem.query.filter_by(pay_order_id=id).first()
    address_info = MemberAddres.query.filter_by(member_id=member_info.id).first()

    if not pay_info:
        return redirect(UrlManager.buildUrl("/finance/index"))
    if not member_info:
        return redirect(UrlManager.buildUrl("/finance/index"))
    if not pay_item_info:
        return redirect(UrlManager.buildUrl("/finance/index"))

    ids = [id]
    pay_item_map = getDictList(PayOrderItem, PayOrderItem.pay_order_id, "pay_order_id", ids)
    pay_item_list = []
    if pay_item_map:
        pay_item_list = pay_item_map[id]

    food_mapping = getDict(Food, Food.id, "id", [])

    resp_data['pay_info'] = pay_info
    resp_data['pay_item_list'] = pay_item_list
    resp_data['food_mapping'] = food_mapping
    resp_data['member_info'] = member_info
    resp_data['address_info'] = address_info
    resp_data['current'] = 'index'
    return ops_render( "finance/pay_info.html",resp_data)


@route_finance.route( "/account" )
def account():
    resp_data = {}
    req = request.values
    query = PayOrder.query

    pay_list = query.order_by(PayOrder.id.asc()).all()
    price = 0
    for item in pay_list:
        price += item.total_price

    resp_data['price'] = price
    resp_data['info'] = pay_list
    return ops_render( "finance/account.html",resp_data )


@route_finance.route( "/ops", methods=["POST"])
def ops():
    prompt = {'code': 200, 'msg': '确认成功', 'data': {}}
    req = request.values

    id = req['id'] if 'id' in req else 0
    act = req['act'] if 'act' in req else ''

    info = PayOrder.query.filter_by(id=id).first()

    if not info:
        prompt['code'] = -1
        prompt['msg'] = "系统繁忙！"
        return jsonify(prompt)

    if act == "express":
        info.status = 1

    db.session.add(info)
    db.session.commit()
    return jsonify(prompt)


def dataList(pay_list):

    data_list = []

    if pay_list:
        pay_order_ids = selectFilter(pay_list, "id")
        pay_order_item_map = getDictList(PayOrderItem, PayOrderItem.pay_order_id, "pay_order_id", pay_order_ids)

        food_mapping = {}
        if pay_order_item_map:
            food_ids = []
            for item in pay_order_item_map:
                food_id = selectFilter(pay_order_item_map[item], "food_id")
                # food_ids_tmp = {}.fromkeys(food_ids_tmp).values()
                food_ids += food_id

            food_mapping = getDict(Food, Food.id, "id", food_ids)

            for item in pay_list:
                member_info = Member.query.filter_by(id=item.member_id).first()
                data_tmp = {
                    "id": item.id,
                    "nickname": member_info.nickname,
                    "status_desc": item.status_desc,
                    "order_number": item.order_sn,
                    "price": item.total_price
                }

                food_tmp = []
                pay_order_item = pay_order_item_map[item.id]
                for tmp in pay_order_item:
                    food_info = food_mapping[tmp.food_id]
                    member_info = Member.query.filter_by(id=food_info.member_id).first()
                    food_tmp.append({
                        "name": food_info.name,
                        "quantity": tmp.quantity,
                        "merchants": member_info.nickname
                    })
                data_tmp['foods'] = food_tmp
                data_list.append(data_tmp)

    return data_list
