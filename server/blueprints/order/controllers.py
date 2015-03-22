#coding=utf-8
from __future__ import absolute_import
from flask import current_app, g
from bson import ObjectId
from utils.base_utils import output_json, generate_current_second
from utils.request import parse_request_body
from errors.validation_errors import ObjectIdStructure, PriceStructure, MinorDescStructure, ValidationParameterRequired
from errors.bp_orders_errors import OrderNotFound, ItemNotFound, VerifyGroupError


def _get_items_info(items_id_list):
    items = current_app.mongodb_conn.Item.find_all_by_id_list(items_id_list)
    order_items = []
    for item in items:
        order_items.append({
            "id": item['_id'],
            "user": _get_user_info(item['user']),
            "fee": item['fee'],
            "note": item['note'],
        })
    return order_items


def _get_user_info(user_id):
    user = current_app.mongodb_conn.User.find_one_by_id(user_id)
    return {
        'id': user['_id'],
        'email': user['email'],
        'nickname': user['nickname'],
        'desc': user['desc'],
    }


@output_json
def get_order(gid):
    group_id = g.current_group['_id']
    orders = current_app.mongodb_conn.Order.find_all_by_group(group_id)
    if orders is None:
        raise OrderNotFound
    group_order = []
    for order in orders:
        group_order.append({
            "id": order['_id'],
            "group": order['group'],
            "createAt": order['createAt'],
            "payer": _get_user_info(order['payer']),
            "total_fee": order['total_fee'],
            "desc": order['desc'],
            "items": _get_items_info(order['items'])
        })
    return {
        'group_order': group_order
    }


'''
request json: payer, total_fee, desc, items
'''
@output_json
def add_order(gid):
    req = parse_request_body()
    payer, total_fee, desc, items = req.get_required_params('payer', 'total_fee', 'desc', 'items')

    # verify order params
    ObjectIdStructure(payer)
    payer_id = ObjectId(payer)
    PriceStructure(total_fee)
    MinorDescStructure(desc)

    # verify items params
    for item in items:
        if not 'user' and 'fee' and 'note' in item:
            raise ValidationParameterRequired
        ObjectIdStructure(item['user'])
        item['user'] = ObjectId(item['user'])
        PriceStructure(item['fee'])
        MinorDescStructure(item['note'])
    # end

    # save order
    group_id = g.current_group['_id']
    createAt = generate_current_second()
    order = current_app.mongodb_conn.Order()
    order['group'] = group_id
    order['createAt'] = createAt
    order['payer'] = payer_id
    order['total_fee'] = total_fee
    order['desc'] = desc
    order.save()

    # save items
    for item in items:
        new_item = current_app.mongodb_conn.Item()
        new_item['order'] = order['_id']
        new_item['user'] = item['user']
        new_item['fee'] = item['fee']
        new_item['note'] = item['note']
        new_item.save()

    return {
        'id': order['_id']
    }


'''
request json: payer, total_fee, desc, items
'''
@output_json
def update_order(gid, order_id):
    # confirm order_id is exit
    ObjectIdStructure(order_id)
    order_id = ObjectId(order_id)
    order = current_app.mongodb_conn.Order.find_one_by_id(order_id)
    if order is None:
        raise OrderNotFound('Update Order Error, Order Not Found')
    # confirm order belongs to current_group
    if not order['group'] == g.current_group['_id']:
        raise VerifyGroupError('order not in group')

    req = parse_request_body()
    desc = req.get_params('desc')
    payer, total_fee, items = req.get_required_params('payer', 'total_fee', 'items')
    # verify order params
    ObjectIdStructure(payer)
    payer_id = ObjectId(payer)
    PriceStructure(total_fee)
    MinorDescStructure(desc)
    # verify items params
    for item in items:
        if not 'user' and 'fee' and 'note' in item:
            raise ValidationParameterRequired
        ObjectIdStructure(item['user'])
        item['user'] = ObjectId(item['user'])
        PriceStructure(item['fee'])
        MinorDescStructure(item['note'])
    # end

    # delete old items
    for old_item_id in order['items']:
        old_item = current_app.mongodb_conn.Item.find_one_by_id(old_item_id)
        old_item.delete()

    # save new items
    item_id_list = []
    for item in items:
        new_item = current_app.mongodb_conn.Item()
        new_item['user'] = item['user']
        new_item['fee'] = item['fee']
        new_item['note'] = item['note']
        new_item.save()
        item_id_list.append(new_item['_id'])

    # save order
    order['payer'] = payer_id
    order['total_fee'] = total_fee
    order['desc'] = desc
    order['items'] = item_id_list
    order.save()
    return {
        'id': order['_id']
    }


@output_json
def delete_order(gid, order_id):
    # verify params
    ObjectIdStructure(order_id)
    order_id = ObjectId(order_id)
    # end

    order = current_app.mongodb_conn.Order.find_one_by_id(order_id)
    if order is None:
        raise OrderNotFound('Delete Group Order Error')
    items = current_app.mongodb_conn.Item.find_all_by_id_list(order['items'])
    for item in items:
        item.delete()

    order.delete()
    return {
        'id': order['_id']
    }
