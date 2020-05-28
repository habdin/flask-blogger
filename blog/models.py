#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module to define the different classes and the corresponding methods for
different database tables for Blogger Flask App"""


from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from blog import db, login


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    """Defines the various fields and methods for the User database table"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref="author", lazy="dynamic")

    def __repr__(self):
        """Defines how new user instance is represented for debugging"""
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        """Creates and stores password hash into the password_hash User database
        field from the password that the user provides on user registration."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks the user password provided on user login forms against the
        password hash stored into the password_hash field in the User database
        table."""
        return check_password_hash(self.password_hash, password)


class Post(db.Model):
    """Defines the various fields and methods for the Post database table"""
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        """Defines how new post instance is represented for debugging"""
        return '<Post {}>'.format(self.body)
