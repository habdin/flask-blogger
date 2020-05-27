#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module to define the different classes and the corresponding methods for
different database tables for Blogger Flask App"""


from datetime import datetime
from blog import db


class User(db.Model):
    """Defines the various fields and methods for the User database table"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref="author", lazy="dynamic")

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Post(db.Model):
    """Defines the various fields and methods for the Post database table"""
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)
