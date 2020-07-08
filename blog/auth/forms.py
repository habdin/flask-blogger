#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Defines various classes and fields for authentication with the auth
blueprint"""

from flask_wtf import FlaskForm
from flask_babel import _, lazy_gettext as _l
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
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
    username = StringField(_l('Username'), validators=[DataRequired()])
    password = PasswordField(_l('Password'),
                             validators=[DataRequired(), Length(min=8)])
    remember_me = BooleanField(_l('Remember Me'))
    submit = SubmitField(_l('Login'))


class RegistrationForm(FlaskForm):
    """Class that defines the fields and methods for registering new users
    in the Blogger Flask App."""
    username = StringField(_l('Username'), validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('Password'),
                             validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField(
        _l('Confirm Password'),
        validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('Register'))

    def validate_username(self, username):
        """Check if the username already exists in the User database."""
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(_('Please choose another username'))

    def validate_email(self, email):
        """Check if the email already exists in the User database."""
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(_('Please choose another email address'))


class ResetPasswordRequestForm(FlaskForm):
    """Class that defines fields for reset password requests from registered
    user that have a forgotten password.
    """
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    submit = SubmitField(_l('Request Password Reset'))


class ResetPasswordForm(FlaskForm):
    """Class that defines fields for resetting password form after successful
    token validation."""
    password = PasswordField(
        _l('Password'), validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField(_l('Confirm Password'),
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField(_l('Request Password Reset'))
