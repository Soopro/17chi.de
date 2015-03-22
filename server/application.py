#coding=utf-8
from __future__ import absolute_import
from flask import Flask, request, current_app, g
from mongokit import Connection
from utils.base_utils import make_json_response, make_cors_headers
from utils.encoders import Encoder
from config import DevelopmentConfig, TestingConfig, ProductionConfig
from errors.general_errors import ErrUncaughtException, NotFound, MethodNotAllowed
import traceback


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}


def create_app(config_name='development'):
    app = Flask(__name__)

    # config
    app.config.from_object(config[config_name])
    app.debug = app.config.get('DEBUG')
    app.json_encoder = Encoder           # bson.ObjectId, encode as string repr

    # database connections
    mongodb_database = Connection(host=app.config.get("MONGODB_HOST"),
                                  port=app.config.get("MONGODB_PORT"))
    mongodb_conn = mongodb_database[app.config.get("MONGODB_DATABASE")]

    # inject database connections to app object
    app.mongodb_database = mongodb_database
    app.mongodb_conn = mongodb_conn


    # register error handlers
    @app.errorhandler(404)
    def app_error_404(error):
        current_app.logger.warn("Error: 404\n{}".format(traceback.format_exc()))
        return make_json_response(NotFound())

    @app.errorhandler(405)
    def app_error_405(error):
        current_app.logger.warn("Error: 405\n{}".format(traceback.format_exc()))
        return make_json_response(MethodNotAllowed())

    @app.errorhandler(400)
    def app_error_400(error):
        current_app.logger.warn("Error: 400\n{}".format(traceback.format_exc()))
        return make_json_response(ErrUncaughtException(repr(error)))


    # register before request handlers
    @app.before_request
    def app_before_request():
        # cors response
        if request.method == "OPTIONS":
            resp = current_app.make_default_options_response()
            cors_headers = make_cors_headers()
            resp.headers.extend(cors_headers)
            return resp
        return

    # register blueprints
    from blueprints.user import blueprint as user_module
    app.register_blueprint(user_module, url_prefix="/user")

    from blueprints.group import blueprint as group_module
    app.register_blueprint(group_module, url_prefix="/group")

    from blueprints.order import blueprint as order_module
    app.register_blueprint(order_module, url_prefix="/order")
    
    from blueprints.menu import blueprint as menu_module
    app.register_blueprint(menu_module, url_prefix="/menu")

    return app



