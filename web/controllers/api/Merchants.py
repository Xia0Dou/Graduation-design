from web.controllers.api import route_api
from flask import request,jsonify
from application import app,db
import requests,json
from common.models.PayOrder import PayOrder
from common.models.PayOrderItem import PayOrderItem
from common.models.Food import Food
from common.models.FoodCat import FoodCat
from common.libs.member.Member import memberInfo
from common.libs.Helper import getDict,getfilter


@route_api.route("/merchants/index")
def merIndex():
    prompt = {'code':200,"msg":"查询成功","data":{}}
    member_info = memberInfo()
    prompt['data']['info'] = {
        'nickname':member_info.nickname,
        'avatar_url':member_info.avatar,
        'purview': member_info.purview,
        'purview_desc':member_info.purview_desc
    }
    return jsonify(prompt)


@route_api.route("/merchants/cat")
def catList():
    prompt = {'code':200,"msg":"查询成功","data":{}}
    cat_list = FoodCat.query.filter_by(status=1).all()
    data_list = []
    if cat_list:
        for item in cat_list:
            data_list.append(item.name)
    prompt['data']['list'] = data_list
    return jsonify(prompt)


@route_api.route("/merchants/food")
def merchantsFood():
    prompt = {'code':200,"msg":"操作成功","data":{}}
    req = request.values
    query = Food.query.filter_by(status=1)

    member_info = memberInfo()
    food_list = query.filter_by(member_id=member_info.id).order_by(Food.total_count.desc()).all()

    data_food_list = []
    if food_list:
        for item in food_list:
            tmp_data = {
                'id': item.id,
                'name': item.name,
                'price': str(item.price),
                'min_price': str(item.price),
                'pic_url': item.image
            }
            data_food_list.append(tmp_data)
    prompt['data']['list'] = data_food_list

    return jsonify(prompt)


@route_api.route("/merchants/merchants/set",methods=['POST'])
def merchantsCreate():
    prompt = {'code':200,"msg":"操作成功","data":{}}
    req = request.values

    id = int(req['id']) if 'id' in req else 0
    cat = req['cat'] if 'cat' in req else ''
    name = req['name'] if 'name' in req else ''
    price = req['price'] if 'price' in req else ''
    image = req['image'] if 'image' in req else ''
    note = req['note'] if 'note' in req else ''

    member_info = memberInfo()
    cat_map = FoodCat.query.filter_by(status=1).all()
    app.logger.error(cat_map)
    app.logger.error(cat)
    for item in cat_map:
        if item.name == cat:
            cat_id = item.id
        else:
            cat_id = 1

    if id < 1:
        food_info = Food()
        food_info.name = name
        food_info.cat_id = cat_id
        food_info.price = price
        food_info.image = image
        food_info.summary = note
        food_info.member_id = member_info.id

        db.session.add(food_info)
        db.session.commit()
        return jsonify(prompt)

    food_info = Food.query.filter_by(id=id).first()

    food_info.cat_id = cat_id
    food_info.name = name
    food_info.price = price
    food_info.image = image
    food_info.summary = note

    db.session.add(food_info)
    db.session.commit()
    return jsonify(prompt)


@route_api.route("/merchants/delete",methods=['POST'])
def merchantsDelete():
    prompt = {'code':200,"msg":"删除成功","data":{}}
    req = request.values

    id = int(req['id']) if 'id' in req else 0

    food_info = Food.query.filter_by(id=id).first()

    food_info.status = 0

    db.session.add(food_info)
    db.session.commit()
    return jsonify(prompt)


@route_api.route("/merchants/food/info")
def merchantsFoodInfo():
    prompt = {'code':200,"msg":"删除成功","data":{}}
    req = request.values

    id = int(req['id']) if 'id' in req else 0
    if not id:
        prompt['code'] = -1
        prompt['msg'] = "没有信息"
        return jsonify(prompt)

    food_info = Food.query.filter_by(id=id).first()

    data_info = []
    if food_info:
        data_info = {
            'id': food_info.id,
            'name': food_info.name,
            'price': str(food_info.price),
            'image': food_info.image,
            'note': food_info.summary
        }
    app.logger.error(food_info.image)
    prompt['data']['info'] = data_info
    return jsonify(prompt)


@route_api.route("/merchants/order",methods=["GET","POST"])
def merchantsOrderList():
    prompt = {'code': 200, "msg": "操作成功！", "data": {}}
    req = request.values
    member_info = memberInfo()
    if not member_info:
        prompt['code'] = -1
        prompt['msg'] = "操作失败！"
        return jsonify(prompt)

    status = int(req['status']) if 'status' in req else 0

    query = PayOrder.query.filter_by()

    if status == 0:     # 已完成
        query = query.filter(PayOrder.status==0)
    elif status == 1:     # 已支付
        query = query.filter(PayOrder.status==1)
    elif status == 2:     # 待支付
        query = query.filter(PayOrder.status==2)
    elif status == 3:     # 待确认
        query = query.filter(PayOrder.status==3)
    else:
        query = query.filter(PayOrder.status == 4)

    order_list = query.order_by(PayOrder.id.desc()).all()
    pay_order_list = []
    if order_list:
        for item in order_list:
            pay_item = PayOrderItem.query.filter_by(pay_order_id=item.id).first()
            pay_food = Food.query.filter_by(id=pay_item.food_id).first()
            if member_info.id == pay_food.member_id:
                pay_order_list.append(item)

    data_order_list= []
    if pay_order_list:
        order_ids = getfilter(pay_order_list, 'id')
        order_item = PayOrderItem.query.filter(PayOrderItem.pay_order_id.in_(order_ids)).all()
        food_ids = getfilter(order_item,'food_id')
        food_map = getDict(Food,Food.id,"id",food_ids)
        order_item_map = {}
        if order_item:
            for item in order_item:
                if item.pay_order_id not in order_item_map:
                    order_item_map[item.pay_order_id] = []

                food_info = food_map[item.food_id]
                order_item_map[item.pay_order_id].append({
                    'id':item.id,
                    'food_id':item.food_id,
                    'quantity':item.quantity,
                    'pic_url':food_info.image,
                    'name':food_info.name,
                })

        for item in pay_order_list:
            tmp_data = {
                'status':item.status,
                'status_desc':item.status_desc,
                'date':item.pay_time.strftime("%Y-%m-%d %H:%M:%S"),
                'order_number':item.order_sn,
                'note':item.note,
                'total_price':str(item.total_price),
                'goods_list':order_item_map[item.id]
            }
            data_order_list.append(tmp_data)

    prompt['data']['pay_order_list'] = data_order_list

    return jsonify(prompt)


@route_api.route("/merchants/confirm",methods=["POST"])
def merchantsFonfirm():
    prompt = {'code': 200, "msg": "操作成功", "data": {}}
    req = request.values
    order_sn = req['order_sn'] if 'order_sn' in req else ''

    pay_order_info = PayOrder.query.filter_by(order_sn=order_sn).first()
    if not pay_order_info:
        prompt['code'] = -1
        prompt['msg'] = "确认失败！"
        return jsonify(prompt)

    pay_order_info.status = 3
    db.session.add(pay_order_info)
    db.session.commit()
    return jsonify(prompt)
