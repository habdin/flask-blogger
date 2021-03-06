#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Configurator module for Blogger Flask App."""

import os
from dotenv import load_dotenv
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    """Define settings and variables for various Blogger App extensions"""

    # SECRET_KEY is for use with forms mainly
    SECRET_KEY = os.environ.get('SECRET_KEY') or "you-will-never-guess"

    # Environment variables for the database engine
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'blog.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Email Server settings
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['habdin@gmail.com']

    # Pagination Support
    POSTS_PER_PAGE = 10

    # Localization and Internationalization
    LANGUAGES = ['en', 'ar']

    # MS Translator azure service key
    MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')

    # Elasticsearch service configuration
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
