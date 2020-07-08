#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Main Blogger blueprint module file."""

from flask import Blueprint

bp = Blueprint('main', __name__)

from blog.main import routes
