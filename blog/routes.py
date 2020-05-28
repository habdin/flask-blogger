#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module for defining various view functions for the Blogger Flask App."""

from flask import render_template, redirect, flash, url_for, request
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.urls import url_parse
from blog import app, db
from blog.forms import LoginForm, RegistrationForm
from blog.models import User


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    """Home page view function"""
    # Fake user and posts to be removed when true elements of their kinds
    # in the app are created.
    posts = [
        {
            'author': {'username': 'habdin', 'first_name': "Hassan"},
            'body': 'I hope you like your visit to Egypt.'
        },
        {
            'author': {'username': 'jdoe', 'first_name': 'John'},
            'body': 'The weather in Cairo is nice today.'
        }
    ]
    return render_template('index.html', title="Home Page", posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page view function"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title="Login", form=form)


@app.route('/logout')
def logout():
    """Log out cuurent user"""
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User Registration page view function"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
