
from flask import render_template, request, current_app, jsonify
from flask_mail import Message

from main_app import mail
from main_app.core.app_models import BaseResponse
from main_app.core.utils.core_utils import CoreUtils
from main_app.core.utils.tools import Tools
from main_app.userland.controller import mod_userland


@mod_userland.route('/')
def home():
    controller_data = CoreUtils.get_controller_data()
    return render_template('userland/home.html',
                           controller_data=controller_data,
                           current_page='home',
                           title="Home")


@mod_userland.route('/send_mail', methods=['POST'])
def send_mail():
    try:
        response = BaseResponse()
        name = Tools.bleach_clean(request.form['name'].strip())
        email = Tools.bleach_clean(request.form['email'].strip())
        subject = Tools.bleach_clean(request.form['subject'].strip())
        message = Tools.bleach_clean(request.form['message'].strip())

        if not name:
            response.fail(message="Please enter your name!")
        elif not email:
            response.fail(message="Please enter your email!")
        elif not message:
            response.fail(message="Please enter any message!")
        else:
            message = f'From: {email} \n\nMessage:\n{message}'

            mail.send(Message(subject=subject,
                              sender=(name, email),
                              recipients=current_app.config['MAIL_DEFAULT_RECEIVER'].split(','),
                              body=message))
            print('successs')

    except Exception as e:
        response.fail()

    return jsonify(response.__dict__)
