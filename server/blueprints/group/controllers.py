# coding=utf-8
from __future__ import absolute_import
from flask import current_app, g
from bson import ObjectId
from utils.base_utils import output_json
from utils.request import parse_request_body
from errors.general_errors import NotFound, BadRequest
from errors.validation_errors import PrimaryAttrStructure, EmailStructure, ObjectIdStructure, MinorDescStructure
from errors.bp_groups_errors import MemberAlreadyExist, MemberNotFound, CanNotDeleteSelf, OwnerCanNotExit, MemberNotEmpty


@output_json
def get_my_groups():
    user_id = g.current_user['_id']
    relations = current_app.mongodb_conn.Relation.find_all_by_user(user_id)
    if relations is None:
        return {'results': None}
    my_groups = []
    for relation in relations:
        group = current_app.mongodb_conn.Group.find_one_by_id(relation['group'])
        my_groups.append(group)
    return {
        'results':  my_groups,
    }


@output_json
def add_group():
    req = parse_request_body()
    name = req.get_required_params("name")
    desc = req.get_params("desc")
    # verify params
    PrimaryAttrStructure(name, 'name')
    MinorDescStructure(desc, 'desc')
    # end

    #save group
    group = current_app.mongodb_conn.Group()
    group['name'] = name
    group['desc'] = desc
    group.save()

    #save group user relation
    relation = current_app.mongodb_conn.Relation()
    relation['group'] = group['_id']
    relation['user'] = g.current_user['_id']
    relation['role'] = u'owner'
    relation.save()

    return {
        'group': group
    }


@output_json
def get_group_role(gid):
    group_id = g.current_group['_id']
    user_id = g.current_user['_id']
    role = current_app.mongodb_conn.Relation.find_one_by_group_and_user(group_id, user_id)
    return {
        'role': role['role'],
    }


@output_json
def get_group_profile(gid):
    group = g.current_group
    return {
        'group': group,
    }


def _get_user_info_list(user_id_list):
    users = current_app.mongodb_conn.User.find_all_by_id_list(user_id_list)
    user_info_list = []
    for user in users:
        user_info_list.append({
            'id': user['_id'],
            'email': user['email'],
            'nickname': user['nickname'],
            'desc': user['desc'],
        })
    return user_info_list


@output_json
def get_group_member(gid):
    group_members = g.current_group_members
    group_members_info = _get_user_info_list(group_members)
    return {
        'members': group_members_info,
    }


@output_json
def add_group_member(gid):
    req = parse_request_body()
    email, role = req.get_required_params("email", "role")
    # verify params
    EmailStructure(email, 'email')
    if role not in ['owner', 'admin', 'member']:
        raise BadRequest('role error')
    # end
    user = current_app.mongodb_conn.User.find_one_by_email(email)
    if user is None:
        raise NotFound('Add Group Member Error: User Login Not Found')
    if user['_id'] in g.current_group_members:
        raise MemberAlreadyExist('member already exist!')
    relation = current_app.mongodb_conn.Relation()
    relation['group'] = g.current_group['_id']
    relation['user'] = user['_id']
    relation['role'] = role
    relation.save()
    return {
        'id': user['_id'],
    }


@output_json
def delete_group_member(gid, uid):
    # verify params
    ObjectIdStructure(uid, 'uid')
    user_id = ObjectId(uid)
    # end

    # owner can not delete self
    if user_id == g.current_user['_id']:
        raise CanNotDeleteSelf('owner can not delete self before transform RoleOfOwner')
    group_id = g.current_group['_id']
    user = current_app.mongodb_conn.User.find_one_by_id(user_id)
    if user is None:
        raise NotFound('Add group member error: User not found')
    members = g.current_group_members
    if not user['_id'] in members:
        raise MemberNotFound('delete group member error: Member Not Found In Group')
    relation = current_app.mongodb_conn.Relation.find_one_by_group_and_user(group_id, user_id)
    relation.delete()
    return {
        'id': user['_id']
    }


@output_json
def update_group_profile(gid):
    req = parse_request_body()
    name = req.get_required_params("name")
    desc = req.get_params("desc")

    # verify params
    PrimaryAttrStructure(name, 'name')
    MinorDescStructure(desc, 'desc')
    # end

    group = g.current_group
    group['name'] = name
    group['desc'] = desc
    group.save()
    return {
        'id': group['_id'],
    }


@output_json
def transfer_owner_permission(gid):
    req = parse_request_body()
    uid = req.get_required_params("uid")

    # verify params
    ObjectIdStructure(uid, 'uid')
    user_id = ObjectId(uid)
    # end

    user = current_app.mongodb_conn.User.find_one_by_id(user_id)
    if user is None:
        raise NotFound('transfer_owner_permission error: User Not Found')
    group = g.current_group
    if not user['_id'] in group['member']:
        raise MemberNotFound('transfer owner permission error: Member Not Found In Group')
    group['owner'] = user['_id']
    group.save()
    return {
        'owner': group['owner'],
    }

@output_json
def delete_group(gid):
    group = g.current_group
    member = group['member']
    # group should be empty except owner
    if not len(member) == 1:
        raise MemberNotEmpty
    group.delete()
    return {
        'id': group['_id'],
    }
