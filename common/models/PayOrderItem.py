# coding: utf-8
from sqlalchemy import BigInteger, Column, Integer, Numeric, Text
from sqlalchemy.schema import FetchedValue
from application import db


class PayOrderItem(db.Model):
    __tablename__ = 'pay_order_item'

    id = db.Column(db.Integer, primary_key=True)
    pay_order_id = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    member_id = db.Column(db.BigInteger, nullable=False, server_default=db.FetchedValue())
    quantity = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    price = db.Column(db.Numeric(10, 2), nullable=False, server_default=db.FetchedValue())
    food_id = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
