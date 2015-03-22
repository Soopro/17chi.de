# coding=utf-8
from __future__ import absolute_import

from flask import Blueprint, request, current_app
from .routes import urlpatterns
from errors.base_errors import APIError
from utils.base_utils import make_json_response, route_inject

bp_name = "menu"

blueprint = Blueprint(bp_name, __name__)

route_inject(blueprint, urlpatterns)

model_list = []


@blueprint.before_app_first_request
def before_first_request():
    # current_app.mongodb_database.register(model_list)
    return


@blueprint.before_request
def before_request():
    return


# @blueprint.errorhandler(APIError)
# def blueprint_api_err(err):
#     return make_json_response(err)
