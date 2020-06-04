#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module to define the different classes and the corresponding methods for
different database tables for Blogger Flask App"""


from datetime import datetime
from hashlib import md5
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from blog import db, login


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


followers = db.Table('followers',
                     db.Column('follower_id', db.Integer,
                               db.ForeignKey('user.id')),
                     db.Column('followed_id', db.Integer,
                               db.ForeignKey('user.id'))
                     )


class User(UserMixin, db.Model):
    """Defines the various fields and methods for the User database table"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Post', backref="author", lazy="dynamic")
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
    
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

    def avatar(self, size):
        """Grab the user avatar from gravtar web service. The size of the grabbed
        avatar depends on the size which is passed as argument to the avatar
        function"""
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def is_following(self, user):
        """Checks if a user is following another user or not. The function returns
        True or False."""
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def follow(self, user):
        """Make a user follow another user."""
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        """Make a user unfollow another user"""
        if self.is_following(user):
            self.followed.remove(user)

    def followed_posts(self):
        """Returns the posts for followed users of a certain user and
        his (her) own posts in a defined ordered method."""
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id = self.id)
        return followed.union(own).order_by(Post.timestamp.desc())


class Post(db.Model):
    """Defines the various fields and methods for the Post database table"""
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        """Defines how new post instance is represented for debugging"""
        return '<Post {}>'.format(self.body)
