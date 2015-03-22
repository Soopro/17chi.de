#coding=utf-8
from __future__ import absolute_import
from flask import g, current_app, request
from bson import ObjectId
from errors.general_errors import BadRequest, NotFound, PermissionDenied
from errors.bp_groups_errors import GroupMemberRepeated
from errors.validation_errors import ObjectIdStructure


def get_request_group():
    gid = request.view_args.get('gid')
    if gid is None:
        raise BadRequest('GroupID is Required')

    ObjectIdStructure(gid)
    group_id = ObjectId(gid)

    group = current_app.mongodb_conn.Group.find_one_by_id(group_id)
    if group is None:
        raise NotFound('GroupID not Exist')
    return group


# must verify_token() before
# out put:
#     g.current_group_members
#     g.current_group_role
#     g.current_group
def verify_member_permission():
    group = get_request_group()
    group_id = group['_id']
    relations = current_app.mongodb_conn.Relation.find_all_by_group(group_id)
    group_members = []
    count = 0
    for relation in relations:
        group_members.append(relation['user'])
        if g.current_user['_id'] == relation['user']:
            count += 1
            g.current_group_role = relation['role']
    if count > 1:
        raise GroupMemberRepeated
    if g.current_user['_id'] in group_members:
        g.current_group = group
        g.current_group_members = group_members
        return
    else:
        raise PermissionDenied('Need Member Permission')


def verify_owner_permission():
    verify_member_permission()
    if not g.current_group_role == 'owner':
        raise PermissionDenied('Need Owner Permission')


def verify_admin_permission():
    verify_member_permission()
    if not g.current_group_role == 'admin':
        raise PermissionDenied('Need Admin Permission')

