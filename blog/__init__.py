#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Main package file"""

import logging
import os
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_babel import Babel, lazy_gettext as _l
from config import Config

# Initialize Database and migrations extensions
db = SQLAlchemy()
migrate = Migrate()

# Initialize Flask Login extension
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = _l('Please log in to access this page.')

# Initialize Flask-Mail extension
mail = Mail()

# Initialize Flask-Bootstrap extension
bootstrap = Bootstrap()

# Initialize Flask-Moment extension
moment = Moment()

# Initialize Flask-Babel extension
babel = Babel()


# Create Blogger application factory
def create_app(config_class=Config):
    """Blogger Application factory"""

    # Initialize the application
    app = Flask(__name__)

    # Register the configuration module
    app.config.from_object(config_class)

    # Register SQLAlchemy and Database migration with the application factory
    db.init_app(app)
    migrate.init_app(app, db)

    # Register Flask Login with the application factory
    login.init_app(app)

    # Register Flask-Mail with the application factory
    mail.init_app(app)

    # Register Flask-Bootstrap with the application factory
    bootstrap.init_app(app)

    # Register Flask-Moment with the application factory
    moment.init_app(app)

    # Register Flask-Babel with the application factory
    babel.init_app(app)

    # Register different blueprints with the application factory
    from blog.main import bp as main_bp
    app.register_blueprint(main_bp)

    from blog.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from blog.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    if not app.debug and not app.testing:
        # Implement a mail handler for production environment if a mail server
        # exists
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'],
                        app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=[app.config['MAIL_SERVER'], app.config['MAIL_PORT']],
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='Blogger Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        # Implement a logging system handler for production environment if
        # a mail server doesn't exist.
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/blogger.log', maxBytes=10240,
                                           backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Blogger startup')

    return app


@babel.localeselector
def get_locale():
    """Returns a language locale to translate Blogger App to from a predefined
    language list (mostly in the App configuration setting)."""
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])


# Initialize the different modules with the Flask app
# Imports done at the bottom of file to prevent circular imports
from blog import models
