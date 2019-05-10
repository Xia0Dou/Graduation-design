from web.controllers.api import route_api
from flask import request,jsonify
from common.libs.member.Member import memberInfo
from application import app,db
from common.models.MemberAddress import MemberAddres
from common.models.AllAddress import AllAddres


@route_api.route("/my/address/index")
def addressIndex():
    prompt = {'code': 200, "msg": "操作成功", "data": {}}

    member_info = memberInfo()
    address_list = MemberAddres.query.filter_by(status=1,member_id=member_info.id).order_by(MemberAddres.id.asc()).all()

    data_list = []
    if address_list:
        for item in address_list:
            tmp_data = {
                'id': item.id,
                'nickname': item.nickname,
                'mobile': str(item.mobile),
                'is_default': item.is_default,
                'address': item.address
            }
            data_list.append(tmp_data)

    prompt['data']['list'] = data_list

    return jsonify(prompt)


@route_api.route("/my/address/info")
def addressIndfo():
    prompt = {'code': 200, "msg": "操作成功", "data": {}}
    req = request.values
    id = int(req['id']) if 'id' in req and req['id'] else 0

    member_info = memberInfo()
    address_info = MemberAddres.query.filter_by(status=1,id=id,member_id=member_info.id).first()

    data_info = []
    if address_info:
        data_info = {
            'id': address_info.id,
            'nickname': address_info.nickname,
            'mobile': str(address_info.mobile),
            'is_default': address_info.is_default,
            'address': address_info.address
        }
    prompt['data']['info'] = data_info

    return jsonify(prompt)


@route_api.route("/my/address/all")
def addressAll():
    prompt = {'code': 200, "msg": "操作成功", "data": {}}

    address_list = AllAddres.query.filter_by(status=1).order_by(AllAddres.school_id.asc(),AllAddres.grade_id.asc(), AllAddres.class_id.asc()).all()

    data_list = []
    if address_list:
        for item in address_list:
            data_list.append("%s%s%s"%(item.school_str,item.grade_str,item.class_str))

    prompt['data']['list'] = data_list

    return jsonify(prompt)


@route_api.route("/my/address/set",methods = [ "GET","POST" ])
def myAddressSet():
    resp = {'code': 200, 'msg': '操作成功！', 'data': {}}
    req = request.values
    id = int(req['id']) if 'id' in req and req['id'] else 0
    address = req['address'] if 'address' in req else ''
    nickname = req['nickname'] if 'nickname' in req else ''
    mobile = req['mobile'] if 'mobile' in req else ''

    member_info = memberInfo()

    if len(nickname) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入姓名"
        return jsonify(resp)

    if len(mobile) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入手机号"
        return jsonify(resp)

    if not member_info:
        resp['code'] = -1
        resp['msg'] = "系统繁忙！"
        return jsonify(resp)

    address_info = MemberAddres.query.filter_by(id=id, member_id=member_info.id).first()
    if address_info:    # 修改
        model_address = address_info
    else:    # 编辑
        default_address_count = MemberAddres.query.filter_by(is_default=1, member_id=member_info.id, status=1).count()
        model_address = MemberAddres()
        model_address.member_id = member_info.id
        model_address.is_default = 1 if default_address_count == 0 else 0

    model_address.nickname = nickname
    model_address.mobile = mobile

    model_address.school_str = address

    db.session.add(model_address)
    db.session.commit()
    return jsonify(resp)


@route_api.route("/my/address/ops",methods = [ "GET","POST" ])
def myAddressOps():
    resp = {'code': 200, 'msg': '操作成功！', 'data': {}}
    req = request.values
    id = int(req['id']) if 'id' in req and req['id'] else 0
    act = req['act'] if 'act' in req else ''

    member_info = memberInfo()

    if id < 1:
        resp['code'] = -1
        resp['msg'] = "未选择地址"
        return jsonify(resp)

    address_info = MemberAddres.query.filter_by(id=id, member_id=member_info.id).first()
    if act == 'del':
        address_info.status = 0
    else:
        address_list = MemberAddres.query.filter_by(member_id=member_info.id).all()
        if address_list:
            for item in address_list:
                item.is_default = 0
                db.session.add(item)
                db.session.commit()
        address_info.is_default = 1

    db.session.add(address_info)
    db.session.commit()
    return jsonify(resp)




