#coding=utf-8
from __future__ import absolute_import
import httplib

from .base_errors import APIError


class UserLoginOccupied(APIError):
    status_code = httplib.BAD_REQUEST
    status_message = "User_Login_Occupied"
    response_code = 10001


class UserLoginUserNotFound(APIError):
    status_code = httplib.NOT_FOUND
    status_message = "USER_NOT_FOUND"
    response_code = 10002


class WrongPassword(APIError):
    status_code = httplib.UNAUTHORIZED
    response_code = 10003
    status_message = "WRONG_PASSWORD"


class ExtractTokenError(APIError):
    status_code = httplib.INTERNAL_SERVER_ERROR
    response_code = 10004
    status_message = "Extract_Token_Error"


class GenerateTokenError(APIError):
    status_code = httplib.INTERNAL_SERVER_ERROR
    response_code = 10005
    status_message = "Generate_Token_Error"


class TokenSerializerError(APIError):
    status_code = httplib.INTERNAL_SERVER_ERROR
    response_code = 10006
    status_message = "Token_Serializer_Error"
