#coding=utf-8
from __future__ import absolute_import

import httplib
from .base_errors import APIError


# class FileCreateFail(APIError):
#     status_code = httplib.EXPECTATION_FAILED
#     status_message = 'MAKE_FILE_FAILED'
#     response_code = 99001
#
#
# class FileDeleteFail(APIError):
#     status_code = httplib.EXPECTATION_FAILED
#     status_message = 'DELETE_FILE_FAILED'
#     response_code = 99002
#
#
class ValidationError(APIError):
    status_code = httplib.EXPECTATION_FAILED
    response_code = 99003
    status_message = 'INVALID_DATA'


class PasswordMismatch(ValidationError):
    response_code = 99004
    status_message = 'PWD_CONFIRM_NOT_MATCH'


class BadRequest(APIError):
    status_code = httplib.BAD_REQUEST
    status_message = 'BAD_REQUEST'
    response_code = 99005
#
#
# class WrongPassword(BadRequest):
#     response_code = 99006
#     status_message = 'PWD_WRONG'
#
#
# class LackOfRequiredParameter(BadRequest):
#     status_message = 'LACK_REQUIRED_PARAMETER'
#     response_code = 99007
#
#
class PermissionDenied(APIError):
    status_code = httplib.FORBIDDEN
    status_message = 'FORBIDDEN'
    response_code = 99009
#
#
# class PathExist(APIError):
#     status_code = httplib.CONFLICT
#     status_message = 'PATH_CONFLICT'
#     response_code = 99010
#
#
# class AppExist(ValidationError):
#     status_message = 'APP_EXIST'
#     response_code = 99011
#
#
# class ExtensionNotPurchased(BadRequest):
#     status_message = 'EXT_NOT_PURCHASED'
#     response_code = 99012
#
#
# class ExtensionNotActivated(BadRequest):
#     status_message = 'EXT_NOT_ACTIVATED'
#     response_code = 99013
#
#
# class ExtensionAlreadyDeactivated(BadRequest):
#     response_code = 99014
#     status_message = 'EXT_ALREADY_DEACTIVATED'
#
#
# class ExtensionAlreadyActivated(BadRequest):
#     response_code = 99015
#     status_message = 'EXT_ALREADY_ACTIVATED'
#
#
# class ReUploadSameFileName(BadRequest):
#     response_code = 99016
#     status_message = 'REUPLOAD_FILE_DUPLICATE'
#
#
# class InvalidZipFile(BadRequest):
#     response_code = 99017
#     status_message = 'INVALID_ZIP_FILE'
#
#
# class FileAlreadyExist(BadRequest):
#     response_code = 99018
#     status_message = 'FILE_DUPLICATE'
#
#
class NotFound(APIError):
    status_code = httplib.NOT_FOUND
    status_message = 'RESOURCE_NOT_FOUND'
    response_code = 99019
#
#
# class ErrUNAUTHORIZED(APIError):
#     status_code = httplib.UNAUTHORIZED
#     response_code = 99020
#     status_message = "USER_UNAUTHORIZED_ERROR"
#
#
class ErrRequestBodyNotExists(APIError):
    status_code = httplib.BAD_REQUEST
    response_code = 99021
    status_message = "REQUEST_BODY_NOT_EXISTS"
#
#
# class ErrRequestParameterRequired(APIError):
#     status_code = httplib.BAD_REQUEST
#     response_code = 99022
#     status_message = "REQUEST_PARAMETER_REQUIRED"
#
#
# class ErrAppNotFoundOrNotOwner(APIError):
#     status_code = httplib.NOT_FOUND
#     response_code = 99023
#     status_message = "APP_NOT_FOUND"
#
#
# class ErrOtherTypeOfException(APIError):
#     status_code = httplib.INTERNAL_SERVER_ERROR
#     response_code = 99024
#     status_message = "INTERNAL_ERROR"
#
#
# class ErrResponseInstanceTypeError(APIError):
#     status_code = httplib.INTERNAL_SERVER_ERROR
#     response_code = 99025
#     status_message = "API_RESPONSE_TYPE_ERROR"
#
#
class AuthenticationFailed(APIError):
    status_code = httplib.UNAUTHORIZED
    status_message = 'AUTHENTICATION_FAILED'
    response_code = 99026
#
#
# class FileNotFound(APIError):
#     response_code = 99027
#     status_message = 'FILE_NOT_FOUND'
#
#
# class Throttled(APIError):
#     status_code = httplib.BAD_REQUEST
#     status_message = "TOO_MANY_REQUESTS"
#     response_code = 99028
#
#
# class DisplayNameRequired(BadRequest):
#     response_code = 99029
#
#
# class UserLoginOccupied(ValidationError):
#     status_message = "USER_LOG_TAKEN"
#     response_code = 99030
#
#
# class UserAliasOccupied(ValidationError):
#     status_message = "USER_NAME_TAKEN"
#     response_code = 99031
#
#
# class FileFormatNotAllowd(BadRequest):
#     response_code = 99032
#
#
# class ErrResponseDataTypeError(APIError):
#     status_code = httplib.INTERNAL_SERVER_ERROR
#     response_code = 99033
#     status_message = "API_RESPONSE_DATA_ERROR"
#
#
# class TokenLogout(AuthenticationFailed):
#     status_message = 'INVALID_TOKEN'
#     response_code = 99034
#
#
# class NotAllowedExtForTheApp(BadRequest):
#     status_message = 'ACT_EXT_NOT_ALLOWED'
#     response_code = 99035
#

class MethodNotAllowed(APIError):
    response_code = 90036
    status_code = httplib.METHOD_NOT_ALLOWED
    status_message = 'REQUEST_METHOD_NOT_ALLOWED'

#
# class ErrTooManyInviteCodes(APIError):
#     status_code = httplib.BAD_REQUEST
#     response_code = 99037
#     status_message = "too_many_invite_code"
#
#
# class ErrInviteCodeNotExists(APIError):
#     status_code = httplib.BAD_REQUEST
#     response_code = 99038
#     status_message = "invite_code_not_exists"
#
#
# class ErrInviteCodeUsed(APIError):
#     status_code = httplib.BAD_REQUEST
#     response_code = 99039
#     status_message = "invite_code_used"
#
#
# class ErrPublicRegisterNotAllowed(APIError):
#     status_code = httplib.BAD_REQUEST
#     response_code = 99040
#     status_message = "public_register_not_allowed"
#
#
# class EmptyFileName(APIError):
#     status_code = httplib.BAD_REQUEST
#     response_code = 99041
#     status_message = 'EMPTY_FILE_NAME'
#
#
# class AlreadyMaxExtNum(BadRequest):
#     response_code = 90042
#     status_message = 'MAX_EXT_NUM'
#
#
# class EmptyValueNotAllowed(BadRequest):
#     response_code = 90043
#     status_message = 'EMPTY_PARAM_NOT_ALLOWED'
#
#
# class InvalidAlias(BadRequest):
#     response_code = 90044
#     status_message = 'INVALID_ALIAS'
#
#
class ErrInvalidRequestBody(APIError):
    status_code = httplib.BAD_REQUEST
    response_code = 99045
    status_message = "INVALID_REQUEST_BODY"
#
#
# class ErrInvalidObjectId(APIError):
#     status_code = httplib.BAD_REQUEST
#     response_code = 99046
#     status_message = "INVALID_OBJECT_ID"
#
#
class ErrUncaughtException(APIError):
    status_code = httplib.INTERNAL_SERVER_ERROR
    response_code = 99047
    status_message = "UNCAUGHT_EXCEPTION"
#
#
# class ErrInactiveUser(APIError):
#     status_code = httplib.FORBIDDEN
#     response_code = 99048
#     status_message = "INACTIVE_USER"
#
#
# class ErrDomainDuplicated(APIError):
#     status_code = httplib.NOT_FOUND
#     response_code = 99049
#     status_message = "DUPLICATED_DOMAIN"
#
#     def __init__(self, name=""):
#         super(ErrDomainDuplicated, self).__init__(name)
#         return