from flask_restful import Resource, reqparse
from flaskone.api.common import api_success_resp
from flaskone.models import Product as productModel


class Product(Resource):
    def get(self):
        args = reqparse.RequestParser()\
            .add_argument('page_no', type=int)\
            .add_argument('category_id', type=int)\
            .parse_args()
        products = productModel.query.filter_by(status='A')
        if args['category_id']:
            products = products.filter_by(category_id=args['category_id'])
        products = products.paginate(per_page=9, page=args['page_no'], error_out=False)
        prev_page_no = int(products.prev_num or 0)
        next_page_no = int(products.next_num or 0)
        products = [product.api_serialize for product in products.items]
        return api_success_resp(200, 'success', {'products': products, 'prev_page_no': prev_page_no,
                                                 'next_page_no': next_page_no})
