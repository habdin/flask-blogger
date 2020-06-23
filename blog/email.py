#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Email Support Module. It allows to send email for registered users
when errors occur. Errors can be forgotten password, app failure,
notifications and many other conditions."""

from threading import Thread
from flask import render_template
from flask_mail import Message
from flask_babel import _
from blog import mail, app


def send_async_email(app, msg):
    """Function that sends an email to a user asynchronously through
    the Blogger app call."""
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    """Function to send registered users an email for any purpose.
    The function inherists from flask_mail Message class attributes and
    use the mail object defined in the blog app to send the email message
    """
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()


def send_password_reset_email(user):
    """Function that sends password reset email with a password reset token to 
    the user requesting password reset."""
    token = user.get_reset_password_token()
    send_email(_('[Blogger] Reset Your Password'),
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))
