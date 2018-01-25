from flask import Blueprint, render_template, request
from flaskone.models import Product

front_home = Blueprint('front_home', __name__)
BASE_FOLDER = 'front/'


@front_home.route('/', defaults={'page_num': None})
@front_home.route('/<int:page_num>')
def index(page_num):
    products = Product.query.filter_by(status='A')
    if 'category_id' in request.args:
        products = products.filter_by(category_id=request.args.get('category_id'))
    products = products.paginate(per_page=9, page=page_num, error_out=False)
    return render_template(BASE_FOLDER+'home.html', products=products)
