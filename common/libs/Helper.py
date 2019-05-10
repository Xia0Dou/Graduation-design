from flask import g, render_template
from common.libs.user.User_info import userInfo
import datetime
import time

'''
统一模板
'''
def ops_render( template,context = {} ):

    user_info = userInfo()

    g.current_user = None
    if user_info:
        g.current_user = user_info

    if 'current_user' in g:
        context['current_user'] = g.current_user
    return render_template( template, **context )


'''
获取当前时间
'''
def currentDate(format="%y-%m-%d %h:%m:%s"):
    return datetime.datetime.now().strftime(format)

def currentDate1(format="%y%m%d%h%m%s"):
    return time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))


'''
根据key获取相应表的信息
'''
def getDict(db,select,key,id):
    req = {}
    query = db.query
    if id and len(id)>0:
        query = query.filter(select.in_(id))

    list = query.all()
    if not list:
        return req
    for item in list:
        if not hasattr(item,key):
            break
        req[getattr(item,key)] = item
    return req


def selectFilter( obj,field ):
    ret = []
    for item in obj:
        if not hasattr(item, field ):
            break
        if getattr( item,field )  in ret:
            continue
        ret.append( getattr( item,field ) )
    return ret


def getDictList( db,select,key,id ):
    ret = {}
    query = db.query
    if id and len( id ) > 0:
        query = query.filter( select.in_( id ) )

    list = query.all()
    if not list:
        return ret
    for item in list:
        if not hasattr( item,key ):
            break
        if getattr( item,key ) not in ret:
            ret[getattr(item, key)] = []

        ret[ getattr( item,key ) ].append(item )
    return ret


def getfilter(list,id):
    ids = []
    for item in list:
        if not hasattr(item, id):
            break
        if getattr(item, id) in ids:
            continue
        ids.append(getattr(item, id))

    return ids
