#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Defines classes and fields for various forms in the Blogger App."""

from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
    TextAreaField,
    )
from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    EqualTo,
    ValidationError,
    )
from blog.models import User


class LoginForm(FlaskForm):
    """Class that defines the fields for registered user Login Form"""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=8)])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    """Class that defines the fields and methods for registering new users
    in the Blogger Flask App."""
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField(
        'Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField(
            'Confirm Password',
            validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        """Check if the username already exists in the User database."""
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please choose another username')

    def validate_email(self, email):
        """Check if the email already exists in the User database."""
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please choose another email address')


class EditUserProfileForm(FlaskForm):
    """Class that defines fields and methods for edit profiles of registered
    users."""
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About Me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

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
                raise ValidationError('Please use a different username')


class EmptyForm(FlaskForm):
    """Empty form for follow and unfollow users."""
    submit = SubmitField('Submit')
