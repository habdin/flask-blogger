#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module defining how errors messages will be output to the end user of
the Blogger App"""

from flask import render_template
from blog import app, db


@app.errorhandler(404)
def not_found_error(error):
    """Returns the appropriate page for the File Not Found
    error."""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
