from flaskone.app import db
from common.util_sqlalchemy import ResourceMixin
from flaskone.models import Product


class Category(ResourceMixin, db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    status = db.Column(db.CHAR(1), nullable=False)
    products = db.relationship('Product', backref='category', lazy=True)

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title
