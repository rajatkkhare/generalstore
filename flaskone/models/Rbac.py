from flaskone.app import db
from common.util_sqlalchemy import ResourceMixin
from flaskone.models import User

user_roles = db.Table('user_roles',
                      db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                      db.Column('role_id', db.Integer, db.ForeignKey('roles.id'))
                      )


class Role(ResourceMixin, db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    users = db.relationship('User', secondary=user_roles, lazy='subquery', backref=db.backref('roles', lazy=True))

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

