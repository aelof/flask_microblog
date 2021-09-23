from test_app import app
from flask import render_template, flash, redirect, url_for, request 
from test_app.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from test_app.models import User
from werkzeug.urls import url_parse


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:  # current_user is user's object. Value is db's value
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).firts()
        
        # if password wrong or user didn't exists
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        #  save current user for all future pages
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')

        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'username': 'alex'}
    posts = [
        {
            'author': {'username': 'Vanya'},
            'body': 'Beautiful day in Vena'
        },
        {
            'author': {'username': 'Dasha'},
            'body': 'The Nu pogody catroon was cool!'
        },

        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Vena'
        },
        {
            'author': {'username': 'Ипполит'},
            'body': 'Какая гадость эта ваша заливная рыба!'

        },
    ]

    return render_template('index.html', title='Home',
                           user=user, posts=posts)
