from flask import session, redirect, url_for, abort, request
from functools import wraps
from instance.settings import FRONT_LOGIN


def login_required(func=None, login_url=FRONT_LOGIN):
    def decorator(view_func):
        @wraps(view_func)
        def wrap(*args, **kwargs):
            if 'logged_in' in session:
                if session['logged_in']:
                    return view_func(*args, **kwargs)
            return redirect(url_for(login_url))
        return wrap
    if func:
        return decorator(func)
    return decorator


def is_anonymous(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            if session['logged_in']:
                if request.referrer:
                    return redirect(request.referrer)
                return redirect(url_for('front_home.index'))
        return func(*args, **kwargs)
    return wrap


# @has_role(roles=['owner', 'admin']) # Case True
# @has_role(roles='owner') # Case True
# @has_role(roles=['datawriter', 'datareader']) # Case True
# @has_role(roles='datawriter') # Case True
# @has_role(roles=['datareader', 'owner']) # Case True
# @has_role(roles=['owner', 'datareader']) # Case True
# @has_role # Case True
def has_role(func=None, roles=None, require_all=False):
    def decorator(view_func):
        @wraps(view_func)
        def wrap(*args, **kwargs):
            if not roles:
                abort(403)
            user_roles = session['logged_roles']
            if check_role(roles, user_roles, require_all):
                return view_func(*args, **kwargs)
            abort(403)
        return wrap
    if func:
        return decorator(func)
    return decorator


def check_role(role, user_roles, require_all):
    if type(role) is list:
        for role_name in role:
            resp = check_role(role_name, user_roles, require_all)
            if resp and (not require_all):
                return True
            if (not resp) and require_all:
                return False
        # If we've made it this far and require_all is False, then NONE of the roles were found.
        # If we've made it this far and require_all is True, then ALL of the roles were found.
        # Return the value of require_all.
        return require_all
    if role in user_roles:
        return True
    return False
