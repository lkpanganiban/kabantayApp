from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user, logout_user, login_required
from ..models import User
from . import auth
from .forms import LoginForm

@auth.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.verify_password(form.password.data):
			flash('Invalid email or password')
			return redirect(url_for('.login'))
		login_user(user, form.remember_me.data)
		return redirect( url_for('infra.index'))
	return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	flash('You have been logged out.')
	return redirect(url_for('infra.index'))