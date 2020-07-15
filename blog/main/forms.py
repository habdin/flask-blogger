#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Defines classes and fields for forms not related to authentication
within the Blogger App."""

from flask import request
from flask_wtf import FlaskForm
from flask_babel import _, lazy_gettext as _l
from wtforms import (
    StringField,
    SubmitField,
    TextAreaField,
    )
from wtforms.validators import (
    DataRequired,
    Length,
    ValidationError,
    )
from blog.models import User


class SearchForm(FlaskForm):
    """Class that defines the search form field and associated methods."""
    q = StringField(_l('Search'), validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        """
        Init constructor that defines the formdata kwargs and specifically
        disables csrf kwarg.
        """
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)        


class EditUserProfileForm(FlaskForm):
    """Class that defines fields and methods for edit profiles of registered
    users."""
    username = StringField(_l('Username'), validators=[DataRequired()])
    about_me = TextAreaField(_l('About Me'),
                             validators=[Length(min=0, max=140)])
    submit = SubmitField(_l('Submit'))

    def __init__(self, original_username, *args, **kwargs):
        super(EditUserProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        """Checks whether the username provided within the Edit profile form to
        a username that is already present in the username field within the
        User model."""
        if username.data != self.original_username:
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError(_('Please use a different username'))


class EmptyForm(FlaskForm):
    """Empty form for follow and unfollow users."""
    submit = SubmitField('Submit')


class PostForm(FlaskForm):
    """Class that defines fields for making new post from a registered user"""
    post = TextAreaField(_l('Create Post'),
                         validators=[DataRequired(), Length(min=1, max=140)])
    submit = SubmitField(_l('Post'))
