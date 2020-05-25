#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Main package file"""

from flask import Flask

# Initiate the Flask app object
app = Flask(__name__)

# Register the different modules with the Flask app
# Imports done at the bottom of file to prevent circular imports
from blog import routes
