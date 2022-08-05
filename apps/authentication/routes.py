import email
from flask import render_template, redirect, request, url_for, flash
from flask_login import (
    current_user,
    login_user,
    logout_user
)

from apps import db, login_manager
from apps.authentication import blueprint
from apps.authentication.forms import LoginForm, CreateAccountForm, ResetPasswordRequestForm, ResetPasswordForm
from apps.authentication.models import Users

from apps.authentication.util import verify_pass, send_password_reset_email

@blueprint.route('/')
def route_default():
    return redirect(url_for('authentication_blueprint.login'))

#Login
@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:

        # read form data
        username = request.form['username']
        password = request.form['password']

        # Locate user
        user = Users.query.filter_by(username=username).first()

        # Check the password
        if user and verify_pass(password, user.password):

            login_user(user)
            return redirect(url_for('authentication_blueprint.route_default'))

        # Something (user or pass) is not ok
        flash('Wrong user or password', 'danger')
        return render_template('accounts/login.html', msg='Wrong user or password', form=login_form)

    if not current_user.is_authenticated:
        return render_template('accounts/login.html', form=login_form)
    
    return redirect(url_for('home_blueprint.index'))

#Registration
@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    #logout_user()
    #if current_user.is_authenticated:
    #    return redirect(url_for('home_blueprint.index'))

    form = CreateAccountForm()
    if form.validate_on_submit():
        firstname = form.firstname.data
        lastname = form.lastname.data
        username = form.username.data
        email = form.email.data
        password = form.password.data

        #create new user
        user = Users(username=username, email=email, password=password, firstname=firstname, lastname=lastname)
        db.session.add(user)
        db.session.commit()

        # Delete user from session
        logout_user()

        flash('User created successfully', 'info')
        return redirect(url_for('authentication_blueprint.login'))

    return render_template('accounts/register.html', form=form)

#Logout
@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('authentication_blueprint.login')) 

#Reset password request
@blueprint.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('home_blueprint.index'))
    
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password', 'info')
        return redirect(url_for('authentication_blueprint.login'))
    
    return render_template('accounts/reset_password_request.html', title='Reset Password', form=form)

#reset password
@blueprint.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('home_blueprint.index'))

    user = Users.verify_reset_password_token(token)
    if not user:
        flash('Invalid or expired token', 'danger')
        return redirect(url_for('authentication_blueprint.login'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset', 'info')
        return redirect(url_for('authentication_blueprint.login'))
    
    return render_template('accounts/reset_password.html', form=form) 


# Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500
