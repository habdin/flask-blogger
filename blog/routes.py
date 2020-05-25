#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module for defining various view functions for the Blogger Flask App."""

from blog import app


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    """Home page view function"""
    return '<h1>Hello, World!</h1>'
