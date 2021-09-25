from test_app import app, db
from flask import render_template, flash, redirect, url_for, request 
from test_app.forms import LoginForm, RegistrationForm, EditProfileForm
from flask_login import current_user, login_user, logout_user, login_required
from test_app.models import User
from werkzeug.urls import url_parse
from datetime import datetime



@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:  # current_user is user's object. Value is db's value
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
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


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect (url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulatons, you are now a register user')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data 
        db.session.commit()
        flash('Your changes have been saved')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)




@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
            {'author': user, 'body': 'Test post #1'},
            {'author': user, 'body': 'Test post #2'}]

    return render_template('user.html', user=user, posts=posts)        


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()





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

    return render_template('index.html', title='Home', posts=posts)
