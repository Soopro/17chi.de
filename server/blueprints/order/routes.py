#coding=utf-8
from __future__ import absolute_import
from .controllers import *


urlpatterns = [
    # need member permission
    ("/<gid>", get_order, "GET"),
    ("/<gid>", add_order, "POST"),
    ("/<gid>/<order_id>", update_order, "PUT"),       # delete old items, add new items
    ("/<gid>/<order_id>", delete_order, "DELETE")

]