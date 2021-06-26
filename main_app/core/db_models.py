from flask_security import RoleMixin, UserMixin

from main_app import db


class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column('user_id', db.Integer(), db.ForeignKey('user.id'))
    role_id = db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))


class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    phone_number = db.Column(db.String(255))
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(100))
    current_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer)
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    profile_image = db.Column(db.String())
    insert_date = db.Column(db.DateTime())
    timezone = db.Column(db.String(500))
    country = db.Column(db.String(3))
    fs_uniquifier = db.Column(db.String(64), nullable=False)

    roles = db.relationship('Role', secondary='roles_users',
                            backref=db.backref('users', lazy='dynamic'))


class LoginHistory(db.Model):
    __tablename__ = 'login_history'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), index=True)
    is_success = db.Column(db.Boolean)
    login_at = db.Column(db.DateTime, index=True)
    client_ip = db.Column(db.String(100))
    proxy_ip = db.Column(db.String(100))
    browser = db.Column(db.String(40))
    user_agent = db.Column(db.String(200))
    login_message = db.Column(db.String(500))
