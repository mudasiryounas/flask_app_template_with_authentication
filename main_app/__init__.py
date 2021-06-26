import datetime

from flask import Flask, request, session, render_template
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_security import Security, SQLAlchemyUserDatastore
from flask_security.forms import LoginForm
from flask_sqlalchemy import SQLAlchemy

from main_app.core.utils.tools import Tools

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
security = Security()
mail = Mail()


def create_app():
    app = Flask(__name__)

    # configure it in order -> prod overrides prp overrides dev
    app.config.from_pyfile('./config/dev.cfg', silent=True)
    app.config.from_pyfile('./config/prp.cfg', silent=True)
    app.config.from_pyfile('./config/prod.cfg', silent=False)

    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    # configure security
    from main_app.core.db_models import User, Role
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)

    class ExtendentLoginForm(LoginForm):
        def validate(self):
            email = Tools.bleach_clean(request.form['email'])
            if not email:
                self.errors['error'] = ['Login Audit System Prevents You From Login! Please Contact Administrators!']
                return False

            is_success = super(ExtendentLoginForm, self).validate()

            client_ip = None
            client_route_list = request.access_route
            if client_route_list:
                client_ip = Tools.bleach_clean(client_route_list[0])

            try:
                login_message = str(self.errors)
                session['post_login_redirect_url'] = self.next.data

                from main_app.core.db_models import LoginHistory
                proxy_ip = Tools.bleach_clean(request.remote_addr)
                user_agent = Tools.bleach_clean(request.headers.get('User-Agent'))
                email = Tools.bleach_clean(request.form['email'])
                browser = Tools.bleach_clean(request.user_agent.browser)
                login_history = LoginHistory(email=email,
                                             is_success=is_success,
                                             login_at=datetime.datetime.utcnow(),
                                             client_ip=client_ip,
                                             proxy_ip=proxy_ip,
                                             browser=browser,
                                             user_agent=user_agent,
                                             login_message=login_message)
                db.session.add(login_history)
                db.session.commit()

            except:
                is_success = False
                self.errors['error'] = ['Login Audit System Prevents You From Login! Please Contact Administrators!']

            return is_success

    login_manager.init_app(app)
    security_ctx = security.init_app(app=app, datastore=user_datastore,
                                     login_form=ExtendentLoginForm)

    @security_ctx.context_processor
    def security_send_password_reset_notice_context_processor():
        if request.access_route[0]:
            user_ip = Tools.bleach_clean(request.access_route[0])
        else:
            user_ip = Tools.bleach_clean(request.remote_addr)

        user_agent_platform = request.user_agent.platform
        user_agent_version = request.user_agent.version
        user_agent_browser = request.user_agent.browser

        return dict(log_date=datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                    user_ip=user_ip,
                    user_agent_platform=user_agent_platform,
                    user_agent_version=user_agent_version,
                    user_agent_browser=user_agent_browser)

    @app.before_first_request
    def before_first_request():
        from main_app.core.seeds import Seeds
        Seeds.create_default_user_and_roles(user_datastore)

    def __page_unauthorize(e):
        return render_template('401.html'), 401

    def __page_not_found(e):
        return render_template('404.html'), 404

    app.register_error_handler(404, __page_not_found)
    app.register_error_handler(401, __page_unauthorize)

    load_blueprints(app)
    from main_app.core.db_models import User
    return app


def load_blueprints(app):
    from main_app.userland.controller import mod_userland
    from main_app.userland.controllers.home_controller import mod_userland as mod_home
    from main_app.userland.controllers.admin_controller import mod_userland as mod_admin
    app.register_blueprint(mod_userland)
