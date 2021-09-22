from test_app import app
from flask import render_template, flash, redirect, url_for
from test_app.forms import LoginForm


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)



@app.route('/')
@app.route('/index')
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
