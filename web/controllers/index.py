from flask import Blueprint,request
from common.libs.Helper import ops_render
from common.models.Member import Member
from common.models.PayOrder import PayOrder
from application import app

route_index = Blueprint('index_page', __name__)


@route_index.route('/')
def index():
    resp_data = {}
    req = request.values

    member_list = Member.query.order_by().all()
    pay_list = PayOrder.query.order_by().all()

    count = 0
    account = 0
    member_count = {}
    for item in member_list:
        if item.status == 1:
            count += 1
            if item.purview == 1:
                account += 1

    member_count['count'] = count
    member_count['account'] = account
    member_count['merchants'] = count - account

    resp_data['member_count'] = member_count

    total_price = 0
    pay_price = 0
    price = {}
    for item in pay_list:
        pay_price += float(item.pay_price)
        total_price += float(item.total_price)
    price['pay_price'] = pay_price
    price['total_price'] = total_price
    price['yun_price'] = total_price - pay_price

    resp_data['price'] = price
    resp_data['pay_count'] = len(pay_list)

    resp_data['search_con'] = req
    return ops_render("index/index.html",resp_data)
