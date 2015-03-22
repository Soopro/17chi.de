#coding=utf-8
from __future__ import absolute_import
from flask import request, g, current_app
from mongokit import ObjectId
from itsdangerous import TimedJSONWebSignatureSerializer
from werkzeug.security import generate_password_hash, check_password_hash
from errors.bp_users_errors import GenerateTokenError, ExtractTokenError, TokenSerializerError
from errors.general_errors import AuthenticationFailed
from errors.validation_errors import ObjectIdStructure


def serializer():
    try:
        ts = TimedJSONWebSignatureSerializer(
            secret_key='secret_key',
            expires_in=60*60*24*30,         # one month
            algorithm_name='HS256')
    except:
        raise TokenSerializerError
    return ts


def generate_token(uid):
    try:
        token = serializer().dumps(unicode(uid)).decode("utf-8")
    except:
        raise GenerateTokenError
    return token


def extract_token(token):
    try:
        uid = serializer().loads(token)
    except:
        raise ExtractTokenError
    return uid


def verify_token():
    token = request.headers.get('Authorization', None)
    if token is None:
        raise AuthenticationFailed('Authorization Required, Authorization header was missing')
    uid = extract_token(token)

    ObjectIdStructure(uid)
    user_id = ObjectId(uid)

    current_user = current_app.mongodb_conn.User.find_one({'_id': user_id})
    if current_user is None:
        raise AuthenticationFailed("User Not Exist")
    g.current_user = current_user
    return


def generate_hashed_password(password):
    return unicode(generate_password_hash(password))


def check_hashed_password(hashed, password):
    return check_password_hash(str(hashed), password)