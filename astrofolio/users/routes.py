from flask import render_template, url_for, redirect, request, current_app, Blueprint
from astrofolio import db, bcrypt
from astrofolio.models import Admin
from astrofolio.users.forms import LoginForm
from flask_login import login_user, login_required, logout_user

users = Blueprint('users', __name__)

@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(email=form.email.data).first()
        if admin and bcrypt.check_password_hash(admin.password, form.password.data):
            login_user(admin, remember=form.remember.data)
            return redirect(url_for('main.home'))

    return render_template('login.html', title='Login', form=form)

@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('users.login'))
