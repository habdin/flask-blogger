#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Forgotten password Email retrieval module for the Auth blueprint."""


from flask import render_template, current_app
from flask_babel import _
from blog.email import send_email



def send_password_reset_email(user):
    """Function that sends password reset email with a password reset token to
    the user requesting password reset."""
    token = user.get_reset_password_token()
    send_email(_('[Blogger] Reset Your Password'),
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))
