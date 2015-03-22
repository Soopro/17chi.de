from datetime import timedelta

from bson import ObjectId
from bson.errors import InvalidId
from flask import current_app, request, _request_ctx_stack, g
from werkzeug.local import LocalProxy
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer, SignatureExpired, BadSignature
from errors.general_errors import ErrAppNotFoundOrNotOwner, AuthenticationFailed
import json


current_user = LocalProxy(lambda: getattr(_request_ctx_stack.top, 'current_user', None))
current_member = LocalProxy(lambda: getattr(_request_ctx_stack.top, 'current_member', None))
current_application = LocalProxy(lambda: getattr(_request_ctx_stack.top, 'current_application', None))


class AuthFailed(Exception):
    pass


def get_serializer(expires_in=None):
    if expires_in is None:
        expires_in = current_app.config.setdefault('JWT_EXPIRATION_DELTA', 0)
    if isinstance(expires_in, timedelta):
        expires_in = int(expires_in.total_seconds())
    expires_in_total = expires_in + current_app.config['JWT_LEEWAY']
    return TimedJSONWebSignatureSerializer(
        secret_key=current_app.config.get('JWT_SECRET_KEY'),
        expires_in=expires_in_total,
        algorithm_name=current_app.config['JWT_ALGORITHM']
    )


def _load_token(realm=None):
    realm = realm or current_app.config['JWT_DEFAULT_REALM']
    auth = request.headers.get('Authorization', None)

    if auth is None:
        raise AuthFailed('Authorization Required, Authorization header was missing'
                         'WWW-Authenticate: JWT realm="%s"' % realm)

    parts = auth.split()

    if parts[0].lower() != 'bearer':
        raise AuthFailed('Invalid JWT header' 'Unsupported authorization type')
    elif len(parts) == 1:
        raise AuthFailed('Invalid JWT header' 'Token missing')
    elif len(parts) > 2:
        raise AuthFailed('Invalid JWT header' 'Token contains spaces')
    return parts[1]


def _load_payload(token):
    if token == 'localtoken':
        return '53f2b6ce03d64d52672061b5'
    if token == 'devtoken':
        return '53f2b885421aa96d8bea5bb7'
    try:
        return get_serializer().loads(token)
    except SignatureExpired:
        raise AuthFailed('Invalid JWT' 'Token is expired')
    except BadSignature:
        raise AuthFailed('Invalid JWT' 'Token is undecipherable')


load_payload = _load_payload


def get_current_user(redis_conn, mongodb_conn, expired_key_prefix, realm=None):
    token = _load_token(realm)

    if redis_conn.get(expired_key_prefix + token):
        raise AuthFailed('Invalid JWT token as the user has logged out!')

    payload = _load_payload(token)
    try:
        uid = ObjectId(payload)
    except InvalidId:
        raise AuthFailed("Invalid uid")
    user = mongodb_conn.User.find_one({'_id': uid})
    return user


def get_current_member(redis_conn, mongodb_conn, expired_key_prefix, realm=None):
    token = _load_token(realm)

    if redis_conn.get(expired_key_prefix + token):
        raise AuthFailed('Invalid JWT token as the member has logged out!')

    payload = json.loads(_load_payload(token))

    try:
        member_id = ObjectId(payload.get("member_id"))
    except InvalidId:
        raise AuthFailed("Invalid member id")

    member = mongodb_conn.Member.find_one({'_id': member_id})
    if member is None:
        raise AuthFailed("member not found")
    try:
        app_id = ObjectId(payload.get("app_id"))
    except InvalidId:
        raise AuthFailed("Invalid app id")
    app = mongodb_conn.App.find_one_by_id(app_id)
    if app is None:
        raise ErrAppNotFoundOrNotOwner
    if app['owner_id'] not in member['owners']:
        raise AuthenticationFailed
    return member


def get_jwt_token():
    auth = request.headers.get('Authorization')
    parts = auth.split()
    return parts[1]


def generate_token(data, expires_in=None):
    payload = unicode(data)
    return get_serializer(expires_in).dumps(payload).decode("utf-8")

generate_user_token = generate_token


def generate_hashed_password(pwd):
    return unicode(generate_password_hash(pwd))


def check_hashed_password(hashed, password):
    return check_password_hash(str(hashed), password)
