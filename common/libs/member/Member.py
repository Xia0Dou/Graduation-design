from application import app
from flask import request
from common.models.Member import Member


def memberInfo():
    auth_cookie = request.headers.get("Authorization")
    if auth_cookie is None:
        return None
    auth_info = auth_cookie.split("-")

    member_info = Member.query.filter_by(id=auth_info[0]).first()

    return member_info
