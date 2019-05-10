from web.controllers.api import route_api
from flask import request,jsonify
from common.libs.member.Member import memberInfo
from common.libs.PayService import PayService
from common.libs.CartSet import CartSet
from application import app,db
import requests,json,decimal
from common.models.Member import Member
from common.models.MemberAddress import MemberAddres
from common.models.PayOrder import PayOrder
from common.models.PayOrderItem import PayOrderItem
from common.models.Food import Food
from common.libs.Helper import getDict


@route_api.route("/order/index",methods=["POST"])
def orderIndex():
    prompt = {'code': 200, "msg": "操作成功", "data": {}}
    req = request.values
    goods = req['goods'] if 'goods' in req else None

    items = []
    if goods:
        items = json.loads(goods)
    if not items or len(items) < 1:
        prompt['code'] = -1
        prompt['msg'] = "删除失败-1！"
        return jsonify(prompt)

    member_info = memberInfo()
    if not member_info:
        prompt['code'] = -1
        prompt['msg'] = "删除失败-2！"
        return jsonify(prompt)

    food_dic = {}
    for item in items:
        food_dic[item['id']] = item['number']

    food_ids = food_dic.keys()
    food_list = Food.query.filter(Food.id.in_(food_ids)).all()
    data_food_list = []
    yun_price = decimal.Decimal(0.00)
    pay_price = decimal.Decimal(0.00)
    if food_list:
        for item in food_list:
            tmp_data = {
                'id': item.id,
                'name': item.name,
                'price': str(item.price),
                'pic_url': item.image,
                'number': food_dic[item.id]
            }
            pay_price = pay_price + item.price * int(food_dic[item.id])
            data_food_list.append(tmp_data)

    address_info = MemberAddres.query.filter_by(member_id=member_info.id,status=1,is_default=1).first()
    app.logger.error(address_info)
    default_address = {
        'name': address_info.nickname,
        'mobile': address_info.mobile,
        'detail': address_info.address
    }

    prompt['data']['food_list'] = data_food_list
    prompt['data']['pay_price'] = str(pay_price)
    prompt['data']['yun_price'] = str(yun_price)
    prompt['data']['total_price'] = str(pay_price+yun_price)
    prompt['data']['default_address'] = default_address
    return jsonify(prompt)


@route_api.route("/order/create",methods=["POST"])
def orderCreate():
    prompt = {'code': 200, "msg": "操作成功", "data": {}}
    req = request.values
    type = req['type'] if 'type' in req else ''
    goods = req['goods'] if 'goods' in req else None

    items = []
    if goods:
        items = json.loads(goods)
    if not items or len(items) < 1:
        prompt['code'] = -1
        prompt['msg'] = "没有选择商品！"
        return jsonify(prompt)

    member_info = memberInfo()
    target = PayService()
    param = {}
    prompt = target.createOrder(member_info.id,items,param)

    if prompt['code'] == 200 and type == "cart":
        CartSet.deleteItems(member_info.id,items)

    return jsonify(prompt)


@route_api.route("/order/pay",methods=["POST"])
def orderPay():
    prompt = {'code': 200, "msg": "操作成功", "data": {}}
    req = request.values
    order_sn = req['order_sn'] if 'order_sn' in req else ''

    member_info = memberInfo()
    pay_order_info = PayOrder.query.filter_by(order_sn=order_sn,member_id=member_info.id).first()
    if not pay_order_info:
        prompt['code'] = -1
        prompt['msg'] = "支付失败！"
        return jsonify(prompt)

    order_item = PayOrderItem.query.filter_by(pay_order_id=pay_order_info.id).first()
    food_info = Food.query.filter_by(id=order_item.food_id).first()
    merchants_info = Member.query.filter_by(id=food_info.member_id).first()

    info = {
        'orcode': merchants_info.orcode
    }
    prompt['data']['info'] = info
    return jsonify(prompt)


@route_api.route("/order/cancel",methods=["POST"])
def orderCancel():
    prompt = {'code': 200, "msg": "操作成功", "data": {}}
    req = request.values
    order_sn = req['order_sn'] if 'order_sn' in req else ''

    pay_order_info = PayOrder.query.filter_by(order_sn=order_sn).first()
    if not pay_order_info:
        prompt['code'] = -1
        prompt['msg'] = "取消失败-1！"
        return jsonify(prompt)

    target = PayService()
    ret = target.closeOrder(pay_order_id=pay_order_info.id)
    if not ret:
        prompt['code'] = -1
        prompt['msg'] = "取消失败-2！"
        return jsonify(prompt)
    return jsonify(prompt)


@route_api.route("/order/confirm",methods=["POST"])
def orderFonfirm():
    prompt = {'code': 200, "msg": "操作成功", "data": {}}
    req = request.values
    order_sn = req['order_sn'] if 'order_sn' in req else ''

    member_info = memberInfo()
    pay_order_info = PayOrder.query.filter_by(order_sn=order_sn,member_id=member_info.id).first()
    if not pay_order_info:
        prompt['code'] = -1
        prompt['msg'] = "确认失败！"
        return jsonify(prompt)

    pay_order_info.status = 1
    db.session.add(pay_order_info)
    db.session.commit()
    return jsonify(prompt)


@route_api.route("/my/comment/add",methods=["POST"])
def orderComment():
    prompt = {'code': 200, "msg": "评价成功！", "data": {}}
    req = request.values
    order_sn = req['order_sn'] if 'order_sn' in req else ''
    score = req['score'] if 'score' in req else 0
    content = req['content'] if 'content' in req else ''

    member_info = memberInfo()
    pay_order_info = PayOrder.query.filter_by(order_sn=order_sn,member_id=member_info.id).first()
    if not pay_order_info:
        prompt['code'] = -1
        prompt['msg'] = "评价失败！"
        return jsonify(prompt)

    pay_order_info.comment_score = score
    pay_order_info.comment_content = content
    pay_order_info.status = 0

    db.session.add(pay_order_info)
    db.session.commit()
    return jsonify(prompt)

