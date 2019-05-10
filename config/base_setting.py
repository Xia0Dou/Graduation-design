SERVER_PORT = 8999
DEBUG = False
SQLALCHEMY_ECHO = False
AUTH_COOKIE_NAME = "hao_food"

# 小程序ID和秘钥
MINA = {
    "appid": "wxfd8a4978f735aea0",
    "appkey": "474c7b41c869a47d12f380a5b8be9167"
}
# 过滤url  不需要验证
IGNORE_URLS = [
    "^/user/login",
    "^/api"
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
    "0":"商家",
    "2":"审核中"
}

PAY_STATUS_MAPPING = {
    "0": "已完成",
    "1": "待评价",
    "2": "待支付",
    "3": "待确认",
    "4": "已取消",
}



