# -*- coding:UTF-8 -*-
# 封装Flask全局变量，API，数据库
from flask import Flask
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
import os


class Application(Flask):
    def __init__(self,import_name,template_folder=None,root_path=None):
        super(Application,self).__init__(import_name,template_folder=template_folder,root_path=root_path,static_folder=None)       #继承flask的构造函数
        self.config.from_pyfile('config/base_setting.py')   #启用基础环境
        #选择启动环境
        if "ops_config" in os.environ:
            self.config.from_pyfile('config/%s_setting.py'%os.environ['ops_config'])
        db.init_app(self)


db = SQLAlchemy()
app = Application(__name__, template_folder=os.getcwd()+'/web/templates/',root_path=os.getcwd())
manager = Manager(app)


# 模板函数
from common.libs.UrlManager import UrlManager
app.add_template_global(UrlManager.buildStaticUrl,'buildStaticUrl')
app.add_template_global(UrlManager.buildUrl,'buildUrl')