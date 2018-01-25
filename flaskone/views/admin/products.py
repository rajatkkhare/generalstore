from flask import Blueprint, render_template, flash, redirect, url_for, request
from flaskone.app import db
from flaskone.decorators import login_required, has_role
from flaskone.forms.admin_forms import NewProduct, EditProduct
from flaskone.models import Category, Product
from instance.settings import ADMIN_LOGIN, ADMIN_ROLES

product = Blueprint('product', __name__)
BASE_FOLDER = 'admin/products/'


@product.route('', methods=['GET', 'POST'])
@login_required(login_url=ADMIN_LOGIN)
@has_role(roles=ADMIN_ROLES)
def index():
    products = db.session.query(Product.id, Product.name, Product.price, Product.stock, Product.status,
                                Category.title.label('category'))\
        .filter(Product.status != 'X').join(Category).order_by(Product.stock, Product.id.desc())
    categories = Category.query.filter(Category.status != 'X')
    form = NewProduct()
    if request.method == 'POST':
        if form.validate_on_submit():
            p = Product()
            form.populate_obj(p)
            image = request.files['image']
            if image.filename != '':
                filename = p.save_prod_img(image)
                p.resize_prod_img(image, filename)
            p.save()
            flash('Product created successfully.', 'success')
            return redirect(url_for('product.index'))
    return render_template(BASE_FOLDER+'products.html', products=products, categories=categories, form=form)


@product.route('/<int:prod_id>/edit', methods=['GET', 'POST'])
@login_required(login_url=ADMIN_LOGIN)
@has_role(roles=ADMIN_ROLES)
def edit(prod_id):
    prod = Product.query.filter_by(id=prod_id).filter(Product.status != 'X').first_or_404()
    categories = Category.query.filter(Category.status != 'X')
    form = EditProduct()
    if request.method == 'POST':
        if form.validate_on_submit():
            prev_name = prod.image
            form.populate_obj(prod)
            image = request.files['image']
            if image.filename != '':
                filename = prod.save_prod_img(image)
                prod.resize_prod_img(image, filename)
                if prev_name:
                    prod.delete_prod_img(prev_name)
            else:
                prod.image = prev_name if prev_name else ''
            prod.save()
            flash('Product updated successfully.', 'success')
            return redirect(url_for('product.index'))
    return render_template(BASE_FOLDER+'products-edit.html', product=prod, categories=categories, form=form)
