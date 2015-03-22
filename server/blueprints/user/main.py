#coding=utf-8
from __future__ import absolute_import

from flask import Blueprint, request, current_app
from .models import User
from .routes import urlpatterns
from errors.base_errors import APIError
from utils.base_utils import make_json_response, route_inject
from utils.bp_users_utils import verify_token

bp_name = "user"

open_api_endpoints = [
    "{}.register".format(bp_name),
    "{}.login".format(bp_name)]

blueprint = Blueprint(bp_name, __name__)

route_inject(blueprint, urlpatterns)

model_list = [User]


@blueprint.before_app_first_request
def before_first_request():
    current_app.mongodb_database.register(model_list)
    return


@blueprint.before_request
def before_request():
    if request.endpoint in open_api_endpoints:
        return
    verify_token()
    return


@blueprint.errorhandler(APIError)
def blueprint_api_err(err):
    return make_json_response(err)
