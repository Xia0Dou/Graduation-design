# coding: utf-8
from sqlalchemy import BigInteger, Column, DateTime, Integer, String
from sqlalchemy.schema import FetchedValue
from application import db


class Member(db.Model):

    __tablename__ = 'member'

    id = db.Column(db.BigInteger, primary_key=True)
    nickname = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    mobile = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())
    sex = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    avatar = db.Column(db.String(64), nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    purview = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    orcode = db.Column(db.String(64), nullable=False, server_default=db.FetchedValue())
    openid = db.Column(db.String(64), nullable=False, server_default=db.FetchedValue())

    @property
    def sex_desc(self):
        sex_map = {
            "0": "保密",
            "1": "男",
            "2": "女"
        }
        return sex_map[str(self.sex)]

    @property
    def purview_desc(self):
        sex_map = {
            "0": "商家",
            "1": "顾客",
            "2": "审核中",
        }
        return sex_map[str(self.purview)]

    @property
    def status_desc(self):
        status_map = {
            "0": "已删除",
            "1": "正常"
        }
        return status_map[str(self.status)]

