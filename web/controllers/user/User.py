# -*- coding: utf-8 -*-
from flask import Blueprint,request,jsonify,make_response,redirect,g
from common.models.User import User
import json
from application import app,db
from common.libs.UrlManager import UrlManager
from common.libs.Helper import ops_render
from common.libs.user.User_info import userInfo

route_user = Blueprint('user_page',__name__)


# 登录
@route_user.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return ops_render('user/login.html')
        # web/templates/user/login.html

    prompt = {'code': 200, 'msg': '登陆成功', 'data': {}}
    req = request.values
    login_name = req["login_name"] if "login_name" in req else ""
    login_pwd = req["login_pwd"] if "login_pwd" in req else ""

    if login_name is None or len(login_name) < 1:
        prompt['code'] = -1
        prompt['msg'] = "请输入正确的用户名！"
        return jsonify(prompt)

    if login_pwd is None or len(login_pwd) < 1:
        prompt['code'] = -1
        prompt['msg'] = "请输入正确的密码！"
        return jsonify(prompt)

    user_info = User.query.filter_by(login_name=login_name).first()
    if not user_info:
        prompt['code'] = -1
        prompt['msg'] = "请输入正确的用户名和密码-n！"
        return jsonify(prompt)

    if user_info.login_pwd != login_pwd:
        prompt['code'] = -1
        prompt['msg'] = "请输入正确的用户名和密码-p！"
        return jsonify(prompt)

    if user_info.status < 1:
        prompt['code'] = -1
        prompt['msg'] = "用户已失效！"
        return jsonify(prompt)

    response = make_response(json.dumps(prompt))
    response.set_cookie(app.config['AUTH_COOKIE_NAME'], "%s-%s"%(user_info.login_name, user_info.uid))

    return response


# 编辑信息
@route_user.route('/edit',methods=["GET","POST"])
def edit():
    if request.method == "GET":
        return ops_render('user/edit.html',{'current':'edit'})

    prompt = {'code': 200, 'msg': '修改成功', 'data': {}}
    req = request.values
    nickname = req["nickname"] if "nickname" in req else ""
    email = req["email"] if "email" in req else ""

    if nickname is None or len(nickname) < 1:
        prompt['code'] = -1
        prompt['msg'] = "请输入符合规范的姓名！"
        return jsonify(prompt)

    if email is None or len(email) < 1:
        prompt['code'] = -1
        prompt['msg'] = "请输入符合规范的邮箱！"
        return jsonify(prompt)

    user_info = userInfo()
    user_info.nickname = nickname
    user_info.email = email

    db.session.add(user_info)
    db.session.commit()
    return jsonify(prompt)


# 修改密码
@route_user.route('/reset-pwd',methods=["GET","POST"])
def resetPwd():
    if request.method == "GET":
        return ops_render('user/reset_pwd.html',{'current':'reset-pwd'})

    prompt = {'code': 200, 'msg': '修改成功', 'data': {}}
    req = request.values
    old_password = req["old_password"] if "old_password" in req else ""
    new_password = req["new_password"] if "new_password" in req else ""

    if old_password is None or len(old_password) < 4:
        prompt['code'] = -1
        prompt['msg'] = "请输入符合规范的原密码！"
        return jsonify(prompt)

    if new_password is None or len(new_password) < 4:
        prompt['code'] = -1
        prompt['msg'] = "请输入符合规范的新密码！"
        return jsonify(prompt)

    if new_password == old_password:
        prompt['code'] = -1
        prompt['msg'] = "新密码与原密码不能相同，请重新输入！"
        return jsonify(prompt)

    user_info = userInfo()

    if old_password != user_info.login_pwd:
        prompt['code'] = -1
        prompt['msg'] = "原密码错误，请重新输入！"
        return jsonify(prompt)

    user_info.login_pwd = new_password

    db.session.add(user_info)
    db.session.commit()

    response = make_response(json.dumps(prompt))
    response.set_cookie(app.config['AUTH_COOKIE_NAME'], "%s-%s" % (user_info.login_name, user_info.uid))

    return response


# 退出
@route_user.route('/logout')
def logout():
    response = make_response(redirect(UrlManager.buildUrl('/user/login')))
    response.delete_cookie(app.config['AUTH_COOKIE_NAME'])
    return response
