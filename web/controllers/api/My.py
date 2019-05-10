from web.controllers.api import route_api
from flask import request,jsonify
from common.libs.member.Member import memberInfo
from common.libs.CartSet import CartSet
from application import app,db
import requests,json
from common.models.Member import Member
from common.models.PayOrder import PayOrder
from common.models.PayOrderItem import PayOrderItem
from common.models.MemberCart import MemberCart
from common.models.Food import Food
from common.libs.Helper import getDict,getfilter


@route_api.route("/my/order",methods=["GET","POST"])
def myOrderList():
    prompt = {'code': 200, "msg": "操作成功！", "data": {}}
    req = request.values
    member_info = memberInfo()
    if not member_info:
        prompt['code'] = -1
        prompt['msg'] = "操作失败！"
        return jsonify(prompt)

    status = int(req['status']) if 'status' in req else 0
    query = PayOrder.query.filter_by(member_id=member_info.id)

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

    pay_order_list = query.order_by(PayOrder.id.desc()).all()
    data_order_list = []
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



