
from flask import render_template
from flask_security import login_required, roles_accepted

from main_app.core.utils.core_utils import CoreUtils
from main_app.userland.controller import mod_userland


@mod_userland.route('/admin')
@login_required
@roles_accepted('root')
def admin_home():
    controller_data = CoreUtils.get_controller_data()
    return render_template('userland/admin_home.html',
                           controller_data=controller_data,
                           current_page='admin_home',
                           title="Admin Home")
