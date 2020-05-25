#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module for defining various view functions for the Blogger Flask App."""

from flask import render_template
from blog import app


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    """Home page view function"""
    # Fake user and posts to be removed when true elements of their kinds
    # in the app are created.
    user = {'username': 'habdin', 'first_name': 'Hassan'}
    posts = [
        {
            'author': {'username': 'habdin', 'first_name': "Hassan"},
            'body': 'I hope you like your visit to Egypt.'
        },
        {
            'author': {'username': 'jdoe', 'first_name': 'John'},
            'body': 'The weather in Cairo is nice today.'
        }
    ]
    return render_template('index.html', user=user, posts=posts)
