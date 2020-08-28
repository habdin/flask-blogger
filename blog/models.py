#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module to define the different classes and the corresponding methods for
different database tables for Blogger Flask App"""


from time import time
from datetime import datetime
from hashlib import md5
import jwt
import json
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from blog import db, login
from blog.search import add_to_index, remove_from_index, query_index


class SearchableMixin(object):
    """Mixin class that glues Full text search feature and the engine
    that offers it to the model that is the subject for search."""

    @classmethod
    def search(cls, expression, page, per_page):
        """Returns the actual post(s) for their corresponding ids that is
        obtained from query_index function and also returns the total number
        of posts matching the search criteria."""
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted),
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)


db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)


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
    messages_sent = db.relationship('Message',
                                    foreign_keys='Message.sender_id',
                                    backref='author', lazy='dynamic')
    messages_received = db.relationship('Message',
                                        foreign_keys='Message.recipient_id',
                                        backref='recipient', lazy='dynamic')
    last_message_read_time = db.Column(db.DateTime)
    notifications = db.relationship('Notification', backref='user',
                                    lazy='dynamic')
    
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
        his (her) own posts in a defined ordered manner."""
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

    def get_reset_password_token(self, expires_in=600):
        """Returns a password reset token to the calling function. The token
        is available for only 10 min as shown by the function argument
        expires_in.
        """
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        """Checks the validity of the reset password request token and returns
        the user id for valid token."""
        try:
            id = jwt.decode(token,
                            current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    def new_messages(self):
        """Method that is used to show the number of unread messages for a
        user."""
        last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
        return Message.query.filter_by(recipient=self).filter(
            Message.timestamp > last_read_time).count()

    def add_notification(self, name, data):
        self.notifications.filter_by(name=name).delete()
        n = Notification(name=name, payload_json=json.dumps(data), user=self)
        db.session.add(n)
        return n


class Post(SearchableMixin, db.Model):
    """Defines the various fields and methods for the Post database table"""
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    language = db.Column(db.String(5))
    __searchable__ = ['body']

    def __repr__(self):
        """Defines how new post instance is represented for debugging"""
        return '<Post {}>'.format(self.body)


class Message(db.Model):
    """Defines the various fields and methods for the Message database table"""
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def __repr__(self):
        """Defines how new message instance is represented for debugging"""
        return '<Message {}>'.format(self.body)


class Notification(db.Model):
    """Defines the various fields and methods for the Notification db table."""
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.Float, index=True, default=time)
    payload_json = db.Column(db.Text)

    def get_data(self):
        return json.loads(str(self.payload_json))
