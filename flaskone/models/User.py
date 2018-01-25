import datetime
import os
from werkzeug.utils import secure_filename
from flaskone.app import db
from flaskone.utils import random_generator
from common.util_sqlalchemy import ResourceMixin
from werkzeug.security import generate_password_hash, check_password_hash
from PIL import Image


class User(ResourceMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    remember_token = db.Column(db.String(150), nullable=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    avatar = db.Column(db.String(150), nullable=True)
    phone = db.Column(db.String(15), nullable=True)
    address = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.SMALLINT, nullable=False, default=0)
    is_admin = db.Column(db.SMALLINT, nullable=False, default=0)
    is_verified = db.Column(db.SMALLINT, nullable=False, default=0)
    email_token = db.Column(db.String(150), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now,
                           onupdate=datetime.datetime.now)

    STORAGE_PATH = './storage/avatars'
    AVATAR_SIZES = [(360, 230), (20, 10)]

    def __str__(self):
        return self.first_name

    def __repr__(self):
        return self.first_name

    @classmethod
    def find_user(cls, _email=None, _id=None):
        if _email:
            return cls.query.filter_by(email=_email).first()
        if _id:
            return cls.query.filter_by(id=_id).first()
        return None

    def set_password(self):
        self.password = generate_password_hash(self.password)
        return self.password

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save_avatar(self, avatar):
        filename = secure_filename(avatar.filename)
        filename = random_generator(40) + '.' + filename.rsplit('.', 1)[1].lower()
        avatar.save(os.path.join(self.STORAGE_PATH, filename))
        self.avatar = filename
        return filename

    def resize_avatar(self, avatar, filename):
        avatar = Image.open(avatar)
        for val in self.AVATAR_SIZES:
            name = '{}x{}-'.format(val[0], val[1]) + filename
            banner = avatar.resize(val, Image.ANTIALIAS)
            banner.save(os.path.join(self.STORAGE_PATH, name), 'jpeg', quality=95)
