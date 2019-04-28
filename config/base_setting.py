SERVER_PORT = 8889
DEBUG = False
SQLALCHEMY_ECHO = False
AUTH_COOKIE_NAME = "hao_food"

# 过滤url  不需要验证
IGNORE_URLS = [
    "^/user/login"
]

IGNORE_CHECK_LOGIN_URLS = [
    "^/static",
    "^/favicon.ico"
]

STATUS_MAPPING = {
    "1":"正常",
    "0":"已删除"
}

PURVIEW_MAPPING = {
    "1":"顾客",
    "0":"商家"
}

PAY_STATUS_MAPPING = {
    "1": "已支付",
    "2": "待支付",
    "0": "已完成"
}

PAY_STATUS_DISPLAY_MAPPING = {
    "0": "订单完成",
    "1": "已支付",
    "2": "待支付",
    "3": "待发货",
    "4": "待确认",
    "5": "待评价"
}

