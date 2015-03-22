#coding=utf-8
from __future__ import absolute_import
import httplib
from .base_errors import APIError


class MemberAlreadyExist(APIError):
    status_code = httplib.BAD_REQUEST
    response_code = 20001
    status_message = 'Member Already Exist'


class MemberNotEmpty(APIError):
    status_code = httplib.BAD_REQUEST
    response_code = 20002
    status_message = 'Delete Group Error, Member Not Empty, Delete Other Member First'


class MemberNotFound(APIError):
    status_code = httplib.NOT_FOUND
    response_code = 20003
    status_message = 'Member Not Found'


class CanNotDeleteSelf(APIError):
    status_code = httplib.BAD_REQUEST
    response_code = 20004
    status_message = 'Can Not Delete Self, Choose Member Exit API'


class OwnerCanNotExit(APIError):
    status_code = httplib.BAD_REQUEST
    response_code = 20005
    status_message = 'Owner Can Not Exit, Please Transfer Owner Permission First'


class GroupMemberRepeated(APIError):
    status_code = httplib.INTERNAL_SERVER_ERROR
    response_code = 20006
    status_message = 'So Bad! Group Member Is Repeated!'