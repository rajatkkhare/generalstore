import string, random


def front_roles():
    from flaskone.app import db
    from flaskone.models import Role
    from instance.settings import FRONT_ROLES
    return db.session.query(Role).filter(Role.name.in_(FRONT_ROLES))


def random_generator(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))
