import os

DEBUG = os.environ.get('DEBUG_STATUS', True)
SECRET_KEY = 'KdP0g7HY5IsERsAKPGOhwW08sumvdixU4oRAGWTn8zE'  # os.urandom(24)
URL_BASE = os.environ.get('BASE_URL', 'http://localhost:5000')
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', "mysql://root:root@localhost/flaskpro")
# SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', "postgresql://postgres:root@localhost/flaskpro")
SQLALCHEMY_TRACK_MODIFICATIONS = False
FRONT_ROLES = ['datawriter', 'datareader']
ADMIN_ROLES = ['owner', 'admin']
FRONT_LOGIN = "front_auth.login"
ADMIN_LOGIN = "admin_auth.login"
