from flask import Blueprint

route_api = Blueprint('api_page',__name__)
from web.controllers.api.Memer import *
from web.controllers.api.Food import *
from web.controllers.api.Cart import *
from web.controllers.api.Order import *
from web.controllers.api.My import *
from web.controllers.api.Address import *
from web.controllers.api.Merchants import *


@route_api.route('/')
def index():
    return "api"
