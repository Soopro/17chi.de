#coding: utf-8
from __future__ import absolute_import
from mongokit import Document, ObjectId

'''
order is for group,
item is details of order for user,
one order always matchs many item
'''


class Order(Document):
    __collection__ = 'orders'
    structure = {
        "group": ObjectId,
        "createAt": unicode,
        "payer": ObjectId,
        "total_fee": int,
        "desc": unicode,
    }

    def find_one_by_id(self, order_id):
        return self.one({
            "_id": order_id
        })

    def find_all_by_group(self, group_id):
        return self.find({
            "group": group_id
        })


class Item(Document):
    __collection__ = 'items'
    structure = {
        "order": ObjectId,
        "user": ObjectId,
        "fee": int,
        "note": unicode
    }

    required_fields = ['user', 'fee']

    def find_all_by_user(self, user):
        return self.find({
            "user": user
        })
    
    def find_all_by_order(self, order):
        return self.find({
            "order": order
        })