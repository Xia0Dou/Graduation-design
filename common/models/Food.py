# coding: utf-8
from sqlalchemy import Column, Integer, Numeric, String
from sqlalchemy.schema import FetchedValue
from application import db


class Food(db.Model):
    __tablename__ = 'food'

    id = db.Column(db.Integer, primary_key=True)
    cat_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    member_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    name = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    price = db.Column(db.Numeric(10, 2), nullable=False, server_default=db.FetchedValue())
    image = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    summary = db.Column(db.String(10000), nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    total_count = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())

    @property
    def status_desc(self):
        status_map = {
            "0": "已删除",
            "1": "正常"
        }
        return status_map[str(self.status)]

