from web.controllers.api import route_api
from flask import request,jsonify
from application import app,db
import requests,json
from common.models.Member import Member
from common.libs.member.Member import memberInfo


@route_api.route("/member/login",methods=["GET","POST"])
def login():
    prompt = {'code':200,"msg":"登陆成功","data":{}}
    req = request.values
    code = req['code'] if 'code' in req else ''
    if not code or len(code)<1:
        prompt['code'] = -1
        prompt['msg'] = "未接收到code!"
        return jsonify(prompt)

    url = "https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code" \
        .format(app.config['MINA']['appid'], app.config['MINA']['appkey'], code)
    r = requests.get(url)
    res = json.loads(r.text)
    openid = res['openid']

    nickname = req['nickName'] if 'nickName' in req else ''
    sex = req['gender'] if 'gender' in req else 0
    avatar = req['avatarUrl'] if 'avatarUrl' in req else ''

    member_info = Member.query.filter_by(openid=openid).first()
    if member_info:
        if member_info.status != 1:
            prompt['code'] = -1
            prompt['msg'] = "用户已失效!"
            return jsonify(prompt)
        token = "%s-%s" % (member_info.id, member_info.status)
        prompt['data'] = {"token": token}
        return jsonify(prompt)

    model_member = Member()
    model_member.nickname = nickname
    model_member.sex = sex
    model_member.avatar = avatar
    model_member.openid = openid
    model_member.purview = 1
    db.session.add(model_member)
    db.session.commit()

    token = "%s-%s"%(member_info.id,member_info.status)
    prompt['data'] = {"token":token}
    return jsonify(prompt)


@route_api.route("/member/info")
def info():
    prompt = {'code':200,"msg":"查询成功","data":{}}
    member_info = memberInfo()
    prompt['data']['info'] = {
        'nickname':member_info.nickname,
        'avatar_url':member_info.avatar,
        'purview': member_info.purview,
        'purview_desc':member_info.purview_desc
    }
    return jsonify(prompt)


@route_api.route("/member/getPur")
def getPur():
    prompt = {'code':200,"msg":"操作成功","data":{}}
    member_info = memberInfo()

    prompt['data']['purview'] = member_info.purview

    return jsonify(prompt)


@route_api.route("/member/change",methods=["POST"])
def change():
    prompt = {'code':200,"msg":"修改成功","data":{}}
    member_info = memberInfo()

    if member_info.purview == 1:
        member_info.purview = 2
    elif member_info.purview == 2:
        prompt['msg'] = "审核中，请勿重复提交!"
        return jsonify(prompt)
    else:
        member_info.purview = 1

    db.session.add(member_info)
    db.session.commit()

    return jsonify(prompt)

