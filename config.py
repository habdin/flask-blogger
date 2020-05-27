#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Configurator module for Blogger Flask App."""

import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """Define settings and variables for various Blogger App extensions"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or "you-will-never-guess"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'blog.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
