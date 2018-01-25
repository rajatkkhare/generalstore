from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flaskone.decorators import is_anonymous
from flaskone.forms.front_forms import RegisterForm, LoginForm
from flaskone.models import User
from flaskone.utils import front_roles
from instance.settings import FRONT_LOGIN

front_auth = Blueprint('front_auth', __name__)
BASE_FOLDER = 'front/auth/'


@front_auth.route('/login', methods=['GET', 'POST'])
@is_anonymous
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.find_user(_email=request.form.get('email'))
            if user:
                if user.check_password(request.form.get('password')) and user.is_active:
                    session['logged_in'] = True
                    session['logged_user'] = {'first_name': user.first_name, 'user_id': user.id}
                    session['logged_roles'] = tuple(role.name for role in user.roles)
                    return redirect(url_for('front_home.index'))
                flash('Invalid credentials.', 'danger')
            else:
                form.email.errors.append('Couldn\'t find your account.')
    return render_template(BASE_FOLDER+'login.html', form=form)


@front_auth.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('logged_user', None)
    session.pop('logged_roles', None)
    return redirect(url_for(FRONT_LOGIN))


@front_auth.route('/register', methods=['GET', 'POST'])
@is_anonymous
def register():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            u = User()
            form.populate_obj(u)
            u.set_password()
            avatar = request.files['avatar']
            if avatar.filename != '':
                filename = u.save_avatar(avatar)
                u.resize_avatar(avatar, filename)
            for role in front_roles():
                u.roles.append(role)
            u.save()
            flash('You have been registered successfully. Login to continue.', 'success')
            return redirect(url_for('front_auth.login'))
    return render_template(BASE_FOLDER+'register.html', form=form)
