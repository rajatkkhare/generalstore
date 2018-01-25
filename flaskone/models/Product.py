from flaskone.app import db
from common.util_sqlalchemy import ResourceMixin
from flaskone.utils import random_generator
from werkzeug.utils import secure_filename
from PIL import Image
import os
from flask import url_for
from instance.settings import URL_BASE


class Product(ResourceMixin, db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    image = db.Column(db.String(255), nullable=False)
    price = db.Column(db.DECIMAL(10, 2), nullable=False)
    stock = db.Column(db.INTEGER, nullable=False)
    status = db.Column(db.CHAR(1), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)

    STORAGE_PATH = './storage/products'
    PRODUCT_IMG_SIZES = [(262, 175), (424, 330)]

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'image': self.image,
            'price': "%02g" % self.price,
            'stock': self.stock,
            'status': self.status,
            'category': self.category.title
        }

    @property
    def api_serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'image': URL_BASE+url_for('show_file', filename='products/'+self.image) if self.image else '',
            'price': "%02g" % self.price,
            'stock': self.stock,
            'status': self.status,
            'category': self.category.title
        }

    def save_prod_img(self, prod_img):
        filename = secure_filename(prod_img.filename)
        filename = random_generator(40) + '.' + filename.rsplit('.', 1)[1].lower()
        prod_img.save(os.path.join(self.STORAGE_PATH, filename))
        self.image = filename
        return filename

    def resize_prod_img(self, prod_img, filename):
        for val in self.PRODUCT_IMG_SIZES:
            img = Image.open(prod_img)
            name = '{}x{}-'.format(val[0], val[1]) + filename
            img.thumbnail(val, Image.ANTIALIAS)
            img.save(os.path.join(self.STORAGE_PATH, name), 'jpeg', quality=95)

    def delete_prod_img(self, filename):
        os.remove(os.path.join(self.STORAGE_PATH, filename))
        for val in self.PRODUCT_IMG_SIZES:
            name = '{}x{}-'.format(val[0], val[1]) + filename
            os.remove(os.path.join(self.STORAGE_PATH, name))
