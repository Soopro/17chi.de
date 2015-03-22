#coding=utf-8
from __future__ import absolute_import
from flask import current_app, g
from utils.base_utils import output_json
from utils.bp_users_utils import generate_token, generate_hashed_password, check_hashed_password
from utils.request import parse_request_body
from errors.general_errors import PasswordMismatch
from errors.validation_errors import PrimaryAttrStructure, PrimaryDescStructure, PasswordStructure, EmailStructure
from errors.bp_users_errors import UserLoginOccupied, UserLoginUserNotFound, WrongPassword


@output_json
def register():
    req = parse_request_body()
    email, password, password2, nickname = req.get_required_params('email', 'password', 'password2', 'nickname')

    if password != password2:
        raise PasswordMismatch
    # verify params
    EmailStructure(email, 'email')
    PasswordStructure(password, 'password')
    PasswordStructure(password2, 'password2')
    PrimaryAttrStructure(nickname, 'nickname')
    # end

    if current_app.mongodb_conn.User.find_one_by_email(email) is not None:
        raise UserLoginOccupied('Email already exist!')
    user = current_app.mongodb_conn.User()
    user['email'] = email
    user["password"] = generate_hashed_password(password)
    user['nickname'] = nickname
    user.save()
    return {
        'id': user['_id'],
        'email': email,
        'nickname': nickname,
    }


@output_json
def login():
    req = parse_request_body()
    email, password = req.get_required_params("email", "password")
    
    # verify params
    EmailStructure(email, 'email')
    PasswordStructure(password, 'password')
    # end

    user = current_app.mongodb_conn.User.find_one_by_email(email)
    if user is None:
        raise UserLoginUserNotFound('Email not register yet')

    if not check_hashed_password((user["password"]), password):
        raise WrongPassword('login error')
    token = generate_token(user["_id"])
    return {
        'token': token,
        'id': user['_id'],
    }


@output_json
def logout():
    """
    The logout function just return a invalid token,
    The actual work is done in the front end, such as delete the token in cookie,
    In future we may use some other middleware to store invalid tokens if needed.
    """
    return {'token': None}


@output_json
def update_password():
    req = parse_request_body()
    origin_password, password, password2 = req.get_required_params("origin_password", "password", "password2")

    if password != password2:
        raise PasswordMismatch
    # verify params
    PasswordStructure(password, 'password')
    PasswordStructure(password2, 'password2')
    # end

    user = g.current_user
    if not check_hashed_password((user["password"]), origin_password):
        raise WrongPassword('update password error')
    user["password"] = generate_hashed_password(password)
    user.save()
    return {
        'id': user['_id'],
    }


@output_json
def get_user_account():
    user = g.current_user
    return {
        'email': user['email'],
        'nickname': user['nickname'],
        'desc': user['desc'],
    }


@output_json
def update_user_account():
    req = parse_request_body()
    desc = req.get_params("desc")
    nickname = req.get_required_params("nickname")

    # verify params
    PrimaryAttrStructure(nickname, 'nickname')
    PrimaryDescStructure(desc, 'desc')
    # end
    
    user = g.current_user
    user["nickname"] = nickname
    user["desc"] = desc
    user.save()
    return {
        'nickname': user['nickname'],
        'desc': user['desc'],
    }