#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Blogger Flask App runner module"""

from blog import create_app, db, cli
from blog.models import User, Post, Notification, Message


app = create_app()
cli.register(app)


@app.shell_context_processor
def make_shell_context():
    """Configure extra shell context"""
    return {
        'db': db,
        'User': User,
        'Post': Post,
        'Message': Message,
        'Notification': Notification,
    }
