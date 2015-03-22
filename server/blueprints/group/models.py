#coding: utf-8
from __future__ import absolute_import
from mongokit import Document, ObjectId

'''
group模式类似于简化版的Teambition团队，
创建者即为owner，owner可邀请其他user加入group，

以下操作需要owner权限：
1/添加成员（暂时简化为无需对方确认同意）
2/删除成员
3/删除group
4/修改group配置信息
5/转让ownen权限（暂时简化为无需对方确认同意）

以下非核心功能暂不开通：
1/owner权限转让需要对方确认
2/添加group成员，分为邀请+申请，需双方确认
3/事件通知系统，邮件通知or页面通知
4/权限体系分为owner，管理员，普通member三元系统，多管理员方便管理
'''


class Group(Document):
    __collection__ = 'groups'
    structure = {
        'name': unicode,
        'desc': unicode
    }

    def find_one_by_id(self, groupId):
        return self.one({
            "_id": groupId
        })


class Relation(Document):
    __collection__ = 'relations'
    structure = {
        'group': ObjectId,
        'user': ObjectId,
        'role': unicode,    # owner, admin, member
    }

    def find_all_by_group(self, group):
        return self.find({
            "group": group
        })

    def find_all_by_user(self, user):
        return self.find({
            "user": user
        })

    def find_one_by_group_and_user(self, group, user):
        return self.one({
            "group": group,
            "user": user
        })
