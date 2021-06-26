
import datetime
from flask import current_app
from main_app import db
from main_app.core.enums import RoleType


class Seeds:
    @staticmethod
    def create_default_user_and_roles(user_datastore):
        from flask_security import utils as flask_security_utils
        # define default roles and root user if it is not
        user_datastore.find_or_create_role(name=RoleType.ROOT.value, description='Administrator')
        db.session.commit()

        root_email = current_app.config['ROOT_EMAIL']
        root_password = current_app.config['ROOT_PASSWORD']
        if not user_datastore.find_user(email=root_email):
            root_encrypted_password = flask_security_utils.hash_password(root_password)
            user_datastore.create_user(email=root_email, password=root_encrypted_password, roles=[RoleType.ROOT.value], timezone='UTC')
            db.session.commit()



