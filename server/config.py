#coding=utf-8
import os


class Config(object):
    # path
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # DATABASES
    MONGODB_HOST = 'localhost'
    MONGODB_PORT = 27017

    # Other
    SECRET_KEY = 'secret_key'
    
    ALLOW_ORIGINS = ['*']
    ALLOW_CREDENTIALS = False


class DevelopmentConfig(Config):
    DEBUG = True
    MONGODB_DATABASE = 'chi_dev'


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    MONGODB_DATABASE = 'chi_test'


class ProductionConfig(Config):
    DEBUG = False
    MONGODB_DATABASE = 'chi_pro'