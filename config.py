#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Configurator module for Blogger Flask App."""

import os


class Config(object):
    """Define settings and variables for various Blogger App extensions"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or "you-will-never-guess"
