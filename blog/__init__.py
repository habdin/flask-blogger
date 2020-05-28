#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Main package file"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
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

# Register the different modules with the Flask app
# Imports done at the bottom of file to prevent circular imports
from blog import routes, forms, models
