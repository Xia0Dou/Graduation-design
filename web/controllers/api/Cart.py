from web.controllers.api import route_api
from flask import request,jsonify
from common.libs.member.Member import memberInfo
from common.libs.CartSet import CartSet
from application import app,db
import requests,json
from common.models.Member import Member
from common.models.MemberCart import MemberCart
from common.models.Food import Food
from common.libs.Helper import getDict,getfilter


@route_api.route("/cart/index",methods=["GET","POST"])
def cartIndex():
    prompt = {'code': 200, "msg": "操作成功！", "data": {}}

    member_info = memberInfo()
    if not member_info:
        prompt['code'] = -1
        prompt['msg'] = "操作失败！"
        return jsonify(prompt)

    cart_list = MemberCart.query.filter_by(member_id=member_info.id).all()
    cart_info = []
    sum_price = 0
    if cart_list:
        food_map = getDict(Food,Food.id,'id',[])
        for item in cart_list:
            sum_price += food_map[item.food_id].price * item.quantity
            cart_info.append({
                'id':item.id,
                'food_id':item.food_id,
                'name':food_map[item.food_id].name,
                'price':str(food_map[item.food_id].price),
                'number':item.quantity,
                'pic_url':food_map[item.food_id].image,
                'active':True
            })

    prompt['data']['list'] = cart_info
    prompt['data']['sum_price'] = str(sum_price)
    return jsonify(prompt)


@route_api.route("/cart/set",methods=["POST"])
def setCart():
    prompt = {'code': 200, "msg": "添加成功", "data": {}}
    req = request.values
    food_id = int(req['id']) if 'id' in req else 0
    number = int(req['number']) if 'number' in req else 0

    if food_id < 1 or number < 1:
        prompt['code'] = -1
        prompt['msg'] = "添加失败-1!"
        return jsonify(prompt)

    member_info = memberInfo()
    if not member_info:
        prompt['code'] = -1
        prompt['msg'] = "添加失败-2!"
        return jsonify(prompt)

    food_info = Food.query.filter_by(id=food_id).first()
    if not food_info:
        prompt['code'] = -1
        prompt['msg'] = "添加失败-3!"
        return jsonify(prompt)

    ret = CartSet.setItems(member_id=member_info.id,food_id=food_id,number=number)
    if not ret:
        prompt['code'] = -1
        prompt['msg'] = "添加失败-4!"
        return jsonify(prompt)
    return jsonify(prompt)


@route_api.route("/cart/delete",methods=["POST"])
def cartDelete():
    prompt = {'code': 200, "msg": "操作成功！", "data": {}}
    req = request.values
    goods = req['goods'] if 'goods' in req else None

    items = []
    if goods:
        items = json.loads(goods)
    if not items or len(items)<1:
        prompt['code'] = -1
        prompt['msg'] = "删除失败-1！"
        return jsonify(prompt)

    member_info = memberInfo()
    if not member_info:
        prompt['code'] = -1
        prompt['msg'] = "删除失败-2！"
        return jsonify(prompt)

    ret = CartSet.deleteItems(member_id=member_info.id,items=items)
    if not ret:
        prompt['code'] = -1
        prompt['msg'] = "删除失败-3！"
        return jsonify(prompt)
    return jsonify(prompt)


@route_api.route("/cart/error")
def cartError():
    prompt = {'code': 200, "msg": "操作成功", "data": {}}
    req = request.values
    goods = req['goods'] if 'goods' in req else None

    items = []
    if goods:
        items = json.loads(goods)

    member_info = memberInfo()
    if not member_info:
        prompt['code'] = -1
        prompt['msg'] = "未登录！"
        return jsonify(prompt)

    food_dic = {}
    for item in items:
        food_dic[item['id']] = item['number']

    food_ids = food_dic.keys()

    if len(food_ids) != 1:
        prompt['code'] = -1
        prompt['msg'] = "请选择同一商家的菜品！"
        return jsonify(prompt)

    return jsonify(prompt)


