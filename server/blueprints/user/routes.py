#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .controllers import *

urlpatterns = [
    # open api
    ('/register', register, 'POST'),
    ('/login', login, 'POST'),

    # need verify token ...
    ('/logout', logout, 'POST'),
    ('/password', update_password, 'PUT'),
    ('/account', get_user_account, "GET"),
    ('/account', update_user_account, 'PUT'),

]
