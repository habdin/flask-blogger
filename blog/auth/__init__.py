#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Main auth blueprint package init file"""

from flask import Blueprint

bp = Blueprint('auth', __name__)

from blog.auth import routes
