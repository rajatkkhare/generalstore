from inspect import getmembers, isfunction
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_debugtoolbar import DebugToolbarExtension
from flask import send_from_directory
from flask_restful import Api
from common import filters
from flaskone.api.resources import api_bp

db = SQLAlchemy()
csrf = CSRFProtect()
api = Api(api_bp, decorators=[csrf.exempt])


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('settings.py')

    @app.route('/storage/<path:filename>')
    def show_file(filename):
        return send_from_directory('../storage', filename)

    @app.before_first_request
    def create_tables():
        db.create_all()

    register_libraries(app)
    register_blueprints(app)
    register_ctx_proc(app)
    register_error_tpl(app)
    register_filters(app)
    register_api_resources()

    return app


def register_libraries(app):
    db.init_app(app)
    csrf.init_app(app)
    DebugToolbarExtension(app)


def register_blueprints(app):
    app.register_blueprint(api_bp, url_prefix='/api')
    from flaskone.views.front.home import front_home
    app.register_blueprint(front_home)
    from flaskone.views.front.auth import front_auth
    app.register_blueprint(front_auth)
    from flaskone.views.admin.auth import admin_auth
    app.register_blueprint(admin_auth, url_prefix='/admin')
    from flaskone.views.admin.home import admin_home
    app.register_blueprint(admin_home, url_prefix='/admin')
    from flaskone.views.admin.categories import prod_cat
    app.register_blueprint(prod_cat, url_prefix='/admin/categories')
    from flaskone.views.admin.products import product
    app.register_blueprint(product, url_prefix='/admin/products')


def register_ctx_proc(app):
    from flaskone.tml_ctx_proc import get_categories, inject_now, is_logged_in, logged_user
    app.context_processor(get_categories)
    app.context_processor(inject_now)
    app.context_processor(is_logged_in)
    app.context_processor(logged_user)


def register_error_tpl(app):
    """
    Register 0 or more custom error pages (mutates the app passed in).

    :param app: Flask application instance
    :return: None
    """

    def render_status(status):
        """
         Render a custom template for a specific status.
           Source: http://stackoverflow.com/a/30108946

         :param status: Status as a written name
         :type status: str
         :return: None
         """
        # Get the status code from the status, default to a 500 so that we
        # catch all types of errors and treat them as a 500.
        code = getattr(status, 'code', 500)
        return render_template('errors/{0}.html'.format(code)), code

    for error in [404, 403, 500]:
        app.errorhandler(error)(render_status)

    return None


def register_filters(app):
    filters_dict = {name: function for name, function in getmembers(filters) if isfunction(function)}
    app.jinja_env.filters.update(filters_dict)


def register_api_resources():
    from flaskone.api.resources.Product import Product
    api.add_resource(Product, '/products')
