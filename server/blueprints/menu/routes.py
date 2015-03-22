# coding=utf-8
from __future__ import absolute_import
from .controllers import *


urlpatterns = [
    ("/menus", get_menus, "GET"),
    ("/test", test, "GET"),

]
