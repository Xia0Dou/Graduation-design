from application import app
from flask import request
from common.models.User import User


def userInfo():
    cookies = request.cookies
    auth_cookies = cookies[app.config['AUTH_COOKIE_NAME']] if app.config['AUTH_COOKIE_NAME'] in cookies else None
    if auth_cookies is None:
        return None
    auth_info = auth_cookies.split("-")

    user_info = User.query.filter_by(login_name=auth_info[0]).first()

    return user_info
