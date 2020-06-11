#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Main package file"""

import logging
import os
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from config import Config

# Initiate the Flask app object
app = Flask(__name__)

# Register the configuration module
app.config.from_object(Config)

# Register Database and migrations with Blogger Flask App
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Register Flask Login with Blogger Flask App
login = LoginManager(app)
login.login_view = 'login'

# Register Flask-Mail with Blogger Flask App
mail = Mail(app)

# Register Flask-Bootstrap with Blogger Flask App
bootstrap = Bootstrap(app)

if not app.debug:
    # Implement a mail handler for production environment if a mail server
    # exists
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=[app.config['MAIL_SERVER'], app.config['MAIL_PORT']],
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Blogger Failure',
            credentials=auth, secure=secure
        )
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

    # Implement a logging system handler for production environment if a mail
    # server doesn't exist.
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/blogger.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Blogger startup')

# Register the different modules with the Flask app
# Imports done at the bottom of file to prevent circular imports
from blog import routes, forms, models, errors
