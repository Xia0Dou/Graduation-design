# -*- coding: utf-8 -*-
import hashlib,time,random,decimal,json
from application import  app,db
from common.models.Food import Food
from common.models.PayOrder import PayOrder
from common.models.PayOrderItem import PayOrderItem
from common.libs.Helper import currentDate1,currentDate

class PayService():

    def __init__(self):
        pass

    def createOrder(self,member_id,items = None,params = None):
        resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
        pay_price  = decimal.Decimal( 0.00 )
        continue_cnt = 0
        food_ids = []
        for item in items:
            if decimal.Decimal( item['price'] ) < 0 :
                continue_cnt += 1
                continue

            pay_price = pay_price +  decimal.Decimal( item['price'] ) * int( item['number'] )
            food_ids.append( item['id'] )

        if continue_cnt >= len(items ) :
            resp['code'] = -1
            resp['msg'] = '商品为空！'
            return resp

        yun_price = params['yun_price'] if params and 'yun_price' in params else 0
        note = params['note'] if params and 'note' in params else ''
        express_address_id = params['express_address_id'] if params and 'express_address_id' in params else 0
        yun_price = decimal.Decimal( yun_price )
        total_price = pay_price + yun_price
        try:
            # 为了防止并发库存出问题了，我们坐下selectfor update
            tmp_food_list = db.session.query( Food ).filter( Food.id.in_( food_ids ) )\
                .with_for_update().all()

            model_pay_order = PayOrder()
            model_pay_order.order_sn = self.geneOrderSn()
            model_pay_order.member_id = member_id
            model_pay_order.total_price = total_price
            model_pay_order.yun_price = yun_price
            model_pay_order.pay_price = pay_price
            model_pay_order.note = note
            model_pay_order.status = 2
            model_pay_order.express_address_id = express_address_id

            db.session.add( model_pay_order )
            db.session.flush()

            for item in items:

                if decimal.Decimal(item['price']) < 0:
                    raise Exception("下单失败请重新下单!")

                tmp_pay_item = PayOrderItem()
                tmp_pay_item.pay_order_id = model_pay_order.id
                tmp_pay_item.member_id = member_id
                tmp_pay_item.quantity = item['number']
                tmp_pay_item.price = item['price']
                tmp_pay_item.food_id = item['id']
                tmp_pay_item.note = note
                db.session.add( tmp_pay_item )
                db.session.flush()

                food_info = Food.query.filter_by(id=item['id']).first()
                food_info.total_count += 1
                db.session.add(food_info)
                db.session.flush()

                # FoodService.setStockChangeLog( item['id'],-item['number'],"在线购买" )
            db.session.commit()
            resp['data'] = {
                'id' : model_pay_order.id,
                'order_sn' : model_pay_order.order_sn,
                'total_price':str( total_price )
            }
        except Exception as e:
            db.session.rollback()
            print( e )
            resp['code'] = -1
            resp['msg'] = "下单失败请重新下单"
            resp['msg'] = str(e)
            return resp
        return resp

    def closeOrder(self,pay_order_id = 0):
        if pay_order_id < 1:
            return False
        pay_order_info = PayOrder.query.filter_by( id =  pay_order_id ).first()
        if not pay_order_info:
            return False

        pay_order_info.status = 4
        db.session.add( pay_order_info )
        db.session.commit()
        return True

    # def orderSuccess(self,pay_order_id = 0,params = None):
    #     try:
    #         pay_order_info = PayOrder.query.filter_by( id = pay_order_id ).first()
    #         if not pay_order_info or pay_order_info.status not in [ -8,-7 ]:
    #             return True
    #
    #         pay_order_info.pay_sn = params['pay_sn'] if params and 'pay_sn' in params else ''
    #         pay_order_info.status = 1
    #         pay_order_info.express_status = -7
    #         pay_order_info.updated_time = getCurrentDate()
    #         db.session.add( pay_order_info  )
    #
    #
    #         pay_order_items = PayOrderItem.query.filter_by( pay_order_id = pay_order_id ).all()
    #         for order_item in pay_order_items:
    #             tmp_model_sale_log = FoodSaleChangeLog()
    #             tmp_model_sale_log.food_id = order_item.food_id
    #             tmp_model_sale_log.quantity = order_item.quantity
    #             tmp_model_sale_log.price = order_item.price
    #             tmp_model_sale_log.member_id = order_item.member_id
    #             tmp_model_sale_log.created_time = getCurrentDate()
    #             db.session.add( tmp_model_sale_log )
    #
    #         db.session.commit()
    #     except Exception as e:
    #         db.session.rollback()
    #         print(e)
    #         return False
    #
    #     #加入通知队列，做消息提醒和
    #     QueueService.addQueue( "pay",{
    #         "member_id": pay_order_info.member_id,
    #         "pay_order_id":pay_order_info.id
    #     })
    #     return True
    #
    # def addPayCallbackData(self,pay_order_id = 0,type = 'pay',data = ''):
    #     model_callback = PayOrderCallbackData()
    #     model_callback.pay_order_id = pay_order_id
    #     if type == "pay":
    #         model_callback.pay_data = data
    #         model_callback.refund_data = ''
    #     else:
    #         model_callback.refund_data = data
    #         model_callback.pay_data = ''
    #
    #     model_callback.created_time = model_callback.updated_time = getCurrentDate()
    #     db.session.add( model_callback )
    #     db.session.commit()
    #     return True

    def geneOrderSn(self):
        while True:
            str = currentDate1()
            if not PayOrder.query.filter_by( order_sn = str  ).first():
                break
        return str
