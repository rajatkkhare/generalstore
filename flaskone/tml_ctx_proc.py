from flask import session
from sqlalchemy import func, desc
from flaskone.app import db
from flaskone.models import Category, Product


def get_categories():
    categories = db.session.query(Category.id, Category.title, func.count(Product.id).label('total_products'))\
        .filter_by(status='A').join(Product).filter_by(status='A')\
        .group_by(Category.id).order_by(desc('total_products'), Category.id.desc())
    return dict(get_categories=categories)


def inject_now():
    from datetime import datetime
    return {'now': datetime.utcnow()}


def is_logged_in():
    if 'logged_in' in session:
        if session['logged_in']:
            return {'logged_in': True}
    return {'logged_in': False}


def logged_user():
    if 'logged_in' in session:
        if session['logged_in']:
            return {'logged_user': session['logged_user']}
    return {'logged_user': None}
