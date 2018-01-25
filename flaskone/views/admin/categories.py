from flask import Blueprint, render_template, flash, redirect, url_for, request
from sqlalchemy import func, and_
from flaskone.app import db
from flaskone.decorators import login_required, has_role
from flaskone.forms.admin_forms import NewCategory
from flaskone.models import Category, Product
from instance.settings import ADMIN_LOGIN, ADMIN_ROLES

prod_cat = Blueprint('prod_cat', __name__)
BASE_FOLDER = 'admin/categories/'


@prod_cat.route('', methods=['GET', 'POST'])
@login_required(login_url=ADMIN_LOGIN)
@has_role(roles=ADMIN_ROLES)
def index():
    categories = db.session.query(Category.id, Category.title, Category.status)\
        .add_columns(func.count(Product.id).label('total_products'))\
        .join(Product, and_(Category.id == Product.category_id, Product.status != 'X'), isouter=True)\
        .filter(Category.status != 'X').group_by(Category.id).order_by(Category.id.desc())
    form = NewCategory()
    if request.method == 'POST':
        if form.validate_on_submit():
            c = Category()
            form.populate_obj(c)
            c.save()
            flash('Category created successfully.', 'success')
            return redirect(url_for('prod_cat.index'))
    return render_template(BASE_FOLDER+'categories.html', categories=categories, form=form)


@prod_cat.route('/<int:cat_id>/edit', methods=['GET', 'POST'])
@login_required(login_url=ADMIN_LOGIN)
@has_role(roles=ADMIN_ROLES)
def edit(cat_id):
    category = Category.query.filter_by(id=cat_id).filter(Category.status != 'X').first()
    form = NewCategory()
    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(category)
            category.save()
            flash('Category updated successfully.', 'success')
            return redirect(url_for('prod_cat.index'))
    return render_template(BASE_FOLDER+'categories-edit.html', category=category, form=form)
