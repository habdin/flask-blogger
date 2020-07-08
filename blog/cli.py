#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module for defining new Blogger Flask command-line commands"""

import os
import click


def register(app):
    @app.cli.group()
    def translate():
        """Translation and localization commands"""
        pass


    @translate.command()
    def update():
        """Update all languages."""
        # If os.system(command) gives out an exit code other than zero this will
        # signify an error code and thus returning a proper exception is needed
        # from our part. Otherwise the command runs successfully and gives its
        # needed results.
        if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
            raise RuntimeError('extract command failed')
        if os.system('pybabel update -i messages.pot -d blog/translations'):
            raise RuntimeError('update command failed')
        os.remove('messages.pot')

    @translate.command()
    def compile():
        """Compile all languages."""
        if os.system('pybabel compile -d blog/translations'):
            raise RuntimeError('pybabel compile failed')

    @translate.command()
    @click.argument('lang')
    def init(lang):
        """Initialize a new language."""
        if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
            raise RuntimeError('extract command failed')
        if os.system(
                'pybabel init -i messages.pot -d blog/translations -l ' + lang):
            raise RuntimeError('init command failed')
        os.remove('messages.pot')
