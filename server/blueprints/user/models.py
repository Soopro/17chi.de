#coding: utf-8
from __future__ import absolute_import
from mongokit import Document


class User(Document):
    __collection__ = 'users'
    structure = {
        'email': unicode,
        'password': unicode,
        'nickname': unicode,
        'desc': unicode
    }

    required_fields = ['email', 'password', 'nickname']

    def find_one_by_id(self, user_id):
        return self.find_one({
            "_id": user_id
        })

    def find_one_by_email(self, email):
        return self.find_one({
            "email": email
        })

    def find_all_by_id_list(self, user_id_list):
        return self.find({
            '_id': {'$in': user_id_list}
        })
