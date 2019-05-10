from web.controllers.api import route_api
from flask import request,jsonify
from application import app,db
from common.models.Member import Member
from common.models.FoodCat import FoodCat
from common.models.Food import Food
from common.libs.UrlManager import UrlManager
from sqlalchemy import or_
from common.libs.Helper import getDict


@route_api.route("/food/index")
def foodIndex():
    prompt = {'code':200,"msg":"操作成功","data":{}}
    cat_list = FoodCat.query.filter_by(status=1).order_by(FoodCat.weight.desc()).all()
    data_cat_list = []
    data_cat_list.append({
        "id":0,
        "name":"全部"
    })
    if cat_list:
        for item in cat_list:
            tmp_data = {
                'id':item.id,
                'name':item.name
            }
            data_cat_list.append(tmp_data)
    prompt['data']['cat_list'] = data_cat_list

    food_list = Food.query.filter_by(status=1).order_by(Food.total_count.desc()).limit(3).all()
    data_food_list = []
    if food_list:
        for item in food_list:
            tmp_data = {
                'id': item.id,
                'pic_url': item.image
            }
            data_food_list.append(tmp_data)
    prompt['data']['banner_list'] = data_food_list

    return jsonify(prompt)


@route_api.route("/food/merchants")
def merchantsList():
    prompt = {'code':200,"msg":"操作成功","data":{}}
    req = request.values
    query = Member.query.filter_by(purview=0)

    mix_kw = str(req['mix_kw']) if 'mix_kw' in req else ''

    if mix_kw:
        rule = or_(Member.nickname.ilike("%{0}%".format(mix_kw)))
        query = query.filter(rule)

    merchants_list = query.order_by(Member.id.asc()).all()

    data_merchants_list = []
    if merchants_list:
        for item in merchants_list:
            food_info = Food.query.filter_by(member_id=item.id,status=1).first()
            tmp_data = []
            if food_info:
                tmp_data = {
                    'id': item.id,
                    'name': item.nickname,
                    'pic_url': food_info.image
                }
                data_merchants_list.append(tmp_data)
    prompt['data']['list'] = data_merchants_list

    return jsonify(prompt)


@route_api.route("/food/search")
def search():
    prompt = {'code':200,"msg":"操作成功","data":{}}
    req = request.values
    query = Food.query.filter_by(status=1)

    member_id = int(req['member_id']) if 'member_id' in req else 0

    query = query.filter_by(member_id=member_id)
    food_list = query.order_by(Food.total_count.desc()).all()

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


@route_api.route("/food/info",methods=["GET","POST"])
def foodInfo():
    prompt = {'code':200,"msg":"操作成功","data":{}}
    req = request.values
    id = int(req['id']) if 'id' in req else 0
    food_info = Food.query.filter_by(id=id).first()
    cat_info = FoodCat.query.filter_by(id=food_info.cat_id).first()

    if not food_info or food_info.status != 1:
        prompt['code'] = -1
        prompt['msg'] = '美食已下架！'

    prompt['data']['info'] = {
        'id':food_info.id,
        'name':food_info.name,
        'summary':food_info.summary,
        'total_count':food_info.total_count,
        'image':food_info.image,
        'price':str(food_info.price),
        'cat':cat_info.name
    }
    return jsonify(prompt)


