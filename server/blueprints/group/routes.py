# coding=utf-8
from __future__ import absolute_import
from .controllers import *


urlpatterns = [
    ("/mine", get_my_groups, "GET"),
    ("/add", add_group, "POST"),

    # need member permission
    ("/<gid>/role", get_group_role, "GET"),
    ("/<gid>/profile", get_group_profile, "GET"),
    ("/<gid>/member", get_group_member, "GET"),

    # need owner permission
    ("/<gid>/member", add_group_member, "POST"),        # by email
    ("/<gid>/member/<uid>", delete_group_member, "DELETE"),
    ('/<gid>/profile', update_group_profile, 'PUT'),
    ("/<gid>/owner", transfer_owner_permission, "PUT"),
    ("/<gid>", delete_group, "DELETE"),

]
