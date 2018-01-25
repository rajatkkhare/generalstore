from flask import Blueprint, render_template, redirect, request, url_for, flash, session
from flaskone.decorators import is_anonymous
from flaskone.forms.admin_forms import LoginForm
from flaskone.models import User
from instance.settings import ADMIN_LOGIN

admin_auth = Blueprint('admin_auth', __name__)
BASE_FOLDER = 'admin/auth/'


@admin_auth.route('/login', methods=['GET', 'POST'])
@is_anonymous
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.find_user(_email=request.form.get('email'))
            if user:
                if user.check_password(request.form.get('password')) and user.is_active and user.is_admin:
                    session['logged_in'] = True
                    session['logged_user'] = {'first_name': user.first_name, 'user_id': user.id}
                    session['logged_roles'] = tuple(role.name for role in user.roles)
                    return redirect(url_for('admin_home.index'))
                flash('Invalid credentials.', 'danger')
            else:
                form.email.errors.append('Couldn\'t find your account.')
    return render_template(BASE_FOLDER+'login.html', form=form)


@admin_auth.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('logged_user', None)
    session.pop('logged_roles', None)
    return redirect(url_for(ADMIN_LOGIN))
