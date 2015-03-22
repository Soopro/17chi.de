#coding=utf-8
from __future__ import absolute_import

from flask import Blueprint, request, current_app
from .models import Order, Item
from .routes import urlpatterns
from errors.base_errors import APIError
from utils.base_utils import make_json_response, route_inject
from utils.bp_users_utils import verify_token
from utils.bp_groups_utils import verify_member_permission, verify_owner_permission

bp_name = "order"


member_permission_endpoints = [
    "{}.get_order".format(bp_name),
    "{}.add_order".format(bp_name),
    "{}.update_order".format(bp_name),
    "{}.delete_order".format(bp_name)]

owner_permission_endpoints = []


blueprint = Blueprint(bp_name, __name__)

route_inject(blueprint, urlpatterns)

model_list = [Order, Item]


@blueprint.before_app_first_request
def before_first_request():
    current_app.mongodb_database.register(model_list)
    return


@blueprint.before_request
def before_request():

    verify_token()

    if request.endpoint in member_permission_endpoints:
        verify_member_permission()
    if request.endpoint in owner_permission_endpoints:
        verify_owner_permission()
    return


@blueprint.errorhandler(APIError)
def blueprint_api_err(err):
    return make_json_response(err)
