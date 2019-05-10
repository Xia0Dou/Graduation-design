from flask import Blueprint,request,redirect,jsonify
from common.libs.Helper import ops_render
from application import app,db
from common.models.Food import Food
from common.models.FoodCat import FoodCat
from common.models.Member import Member
from common.models.PayOrderItem import PayOrderItem
from common.libs.UrlManager import UrlManager
from common.libs.Helper import getDict,getDictList
from sqlalchemy import or_


route_food = Blueprint( 'food_page',__name__ )


@route_food.route( "/index" )
def index():
    resp_data = {}
    req = request.values
    query = Food.query

    if 'mix_kw' in req:
        rule = or_(Food.name.ilike("%{0}%".format(req['mix_kw'])))
        query = query.filter(rule)

    if 'status' in req and int(req['status']) > -1:
        query = query.filter(Food.status == int(req['status']))

    if 'cat_id' in req and int(req['cat_id']) > -1:
        query = query.filter(Food.cat_id == int(req['cat_id']))

    if 'member_id' in req and int(req['member_id']) > -1:
        query = query.filter(Food.member_id == int(req['member_id']))

    list = query.order_by(Food.status.desc(), Food.id.asc()).all()

    cat_mapping = getDict(FoodCat,'id','id',[])
    member_mapping = getDict(Member, 'id', 'id', [])

    resp_data['list'] = list
    resp_data['search_con'] = req
    resp_data['status_mapping'] = app.config['STATUS_MAPPING']
    resp_data['cat_mapping'] = cat_mapping
    resp_data['member_mapping'] = member_mapping

    return ops_render( "food/index.html" ,resp_data)


@route_food.route( "/info" )
def info():
    resp_data = {}
    req = request.args
    id = int(req.get('id', 0))

    if id < 1:
        return redirect(UrlManager.buildUrl("/food/index"))

    info = Food.query.filter_by(id=id).first()
    if not info:
        return redirect(UrlManager.buildUrl("/food/index"))

    ids = [id]
    order_item_map = getDictList(PayOrderItem, PayOrderItem.food_id, "food_id", ids)
    order_item_list = []
    if order_item_map:
        order_item_list = order_item_map[id]

    count = 0
    for item in order_item_list:
        count += item.quantity
    info.total_count = count

    cat_mapping = getDict(FoodCat, 'id', 'id', [])
    member_mapping = getDict(Member, 'id', 'id', [])
    resp_data['cat_mapping'] = cat_mapping
    resp_data['member_mapping'] = member_mapping
    resp_data['info'] = info
    resp_data['order_item_list'] = order_item_list

    return ops_render( "food/info.html" ,resp_data)


# 删除恢复
@route_food.route('/ops',methods=["POST"])
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

    info = Food.query.filter_by(id=id).first()

    if not info:
        prompt['code'] = -1
        prompt['msg'] = "账号不存在！"
        return jsonify(prompt)

    if act == "remove":
        info.status = 0
    elif act == "recover":
        info.status = 1

    db.session.add(info)
    db.session.commit()
    return jsonify(prompt)


# 分类信息
@route_food.route( "/cat" )
def cat():
    resp_data = {}
    req = request.values
    query = FoodCat.query

    if 'status' in req and int(req['status'])>-1:
        query = query.filter(FoodCat.status==int(req['status']))

    list = query.order_by(FoodCat.status.desc(), FoodCat.id.asc()).all()

    resp_data['list'] = list
    resp_data['search_con'] = req
    resp_data['status_mapping'] = app.config['STATUS_MAPPING']
    resp_data['current'] = 'cat'

    return ops_render("food/cat.html", resp_data)


@route_food.route( "/cat-set",methods=["GET","POST"] )
def catSet():
    if request.method == "GET":
        resp_data = {}
        req = request.args
        id = int(req.get('id', 0))

        info = None

        if id :
            info = FoodCat.query.filter_by(id=id).first()

        resp_data['info'] = info
        resp_data['current'] = 'cat'

        return ops_render("food/cat_set.html", resp_data)

    prompt = {'code': 200, 'msg': '修改成功', 'data': {}}
    req = request.values

    id = req["id"] if "id" in req else 0
    name = req["name"] if "name" in req else ""
    weight = int(req["weight"]) if "weight" in req else 1

    if name is None or len(name)<1:
        prompt['code'] = -1
        prompt['msg'] = "请输入符合规范的分类名！"
        return jsonify(prompt)

    if weight < 1:
        prompt['code'] = -1
        prompt['msg'] = "请输入符合规范的权重，至少不小于1！"
        return jsonify(prompt)

    cat_info = FoodCat.query.filter_by(id=id).first()
    if cat_info:
        food_cat = cat_info
    else:
        food_cat = FoodCat()

    food_cat.name = name
    food_cat.weight = weight

    db.session.add(food_cat)
    db.session.commit()
    return jsonify(prompt)


# 删除恢复分类
@route_food.route('/cat-ops',methods=["POST"])
def catOps():
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

    cat_info = FoodCat.query.filter_by(id=id).first()

    if not cat_info:
        prompt['code'] = -1
        prompt['msg'] = "账号不存在！"
        return jsonify(prompt)

    if act == "remove":
        cat_info.status = 0
    elif act == "recover":
        cat_info.status = 1

    db.session.add(cat_info)
    db.session.commit()
    return jsonify(prompt)
