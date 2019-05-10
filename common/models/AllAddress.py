# coding: utf-8
from sqlalchemy import Column, Integer, String
from sqlalchemy.schema import FetchedValue
from application import db,app



class AllAddres(db.Model):
    __tablename__ = 'all_address'

    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    school_str = db.Column(db.String(50), nullable=False, server_default=db.FetchedValue())
    grade_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    grade_str = db.Column(db.String(50), nullable=False, server_default=db.FetchedValue())
    class_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    class_str = db.Column(db.String(50), nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
