#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Errors Blueprint for Blogger App"""

from flask import Blueprint


bp = Blueprint('errors', __name__)


from blog.errors import handlers
