from csv_shipper import mail
from flask_mail import Message
from flask import url_for


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message(
        subject="CSV_Shipper - Password Reset Request",
        sender="",
        recipients=[user.email],
    )

    msg.body = f"""To reset your password, visit the following link: 
{url_for("users.reset_token", token=token, _external=True)}

If you did not make this request, simply ignore this email and no changes will be made
"""
    return mail.send(msg)  # might not need return statement, need to debug to tell.
