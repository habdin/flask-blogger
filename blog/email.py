#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Email Support Module. It allows to send email for registered users
when errors occur. Errors can be forgotten password, app failure,
notifications and many other conditions."""

from threading import Thread
from flask import current_app
from flask_mail import Message
from blog import mail


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
    Thread(target=send_async_email,
           args=(current_app._get_current_object(), msg)).start()
