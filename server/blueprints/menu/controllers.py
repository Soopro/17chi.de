# coding=utf-8
from __future__ import absolute_import
from flask import request
from utils.base_utils import output_json
from .spider_service import SpiderService

@output_json
def test():

    return {"name":"neo","age":25}

@output_json
def get_menus():
    url = request.args.get('url')
    print url
    spider = SpiderService(url)
    menus = spider.get_menus()
    return menus