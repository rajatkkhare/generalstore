from flask import Blueprint, render_template
from flaskone.decorators import login_required, has_role
from instance.settings import ADMIN_LOGIN, ADMIN_ROLES

admin_home = Blueprint('admin_home', __name__)
BASE_FOLDER = 'admin/'


@admin_home.route('')
@login_required(login_url=ADMIN_LOGIN)
@has_role(roles=ADMIN_ROLES)
def index():
    return render_template(BASE_FOLDER+'home.html')
