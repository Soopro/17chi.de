#coding=utf-8
from __future__ import absolute_import
import httplib

from .base_errors import APIError


class OrderNotFound(APIError):
    status_code = httplib.NOT_FOUND
    response_code = 100111
    status_message = "Item Not Found"


class ItemNotFound(APIError):
    status_code = httplib.NOT_FOUND
    response_code = 100112
    status_message = "Item Not Found"


class ParamsValidationError(APIError):
    status_code = httplib.BAD_REQUEST
    response_code = 100113
    status_message = "Params Validation Error"


class VerifyGroupError(APIError):
    status_code = httplib.BAD_REQUEST
    response_code = 100114
    status_message = "Verify Group Error"