from os import environ, path
from settings import SQLALCHEMY_DATABASE_URI


class Config(object):
    # PostgresSQL
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
