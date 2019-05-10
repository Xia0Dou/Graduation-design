from application import app,db
from common.models.MemberCart import MemberCart


class CartSet():

    @staticmethod
    def setItems(member_id=0,food_id=0,number=0):
        if member_id<1 or food_id<1 or number<1:
            return False

        member_cart_info = MemberCart.query.filter_by(food_id=food_id,member_id=member_id).first()
        if member_cart_info:
            cart_info = member_cart_info
        else:
            cart_info = MemberCart()
            cart_info.member_id = member_id
            cart_info.food_id = food_id
        cart_info.quantity = number
        db.session.add(cart_info)
        db.session.commit()
        return True

    @staticmethod
    def deleteItems(member_id=0, items=None):
        if member_id < 1 or not items:
            return False

        for item in items:
            MemberCart.query.filter_by(food_id=item['id'], member_id=member_id).delete()

        db.session.commit()
        return True




