import os
import secrets
from app import app,mail
from PIL import Image
from app.models import Product
from flask_mail import Message
from flask import render_template
from threading import Thread
from app.config import Config


def save_pic(pic):
    random_hex=secrets.token_hex(16)
    _, f_ext = os.path.splitext(pic.filename)
    new_name=random_hex+f_ext
    path = os.path.join(app.root_path,'static/uploads',new_name)
    pic.save(path)

    output_size=(200,200)
    i = Image.open(pic)
    i.thumbnail(output_size)
    i.save(path)
    return new_name


def save_extra_pics(pic):
    random_hex=secrets.token_hex(16)
    _, f_ext = os.path.splitext(pic.filename)
    new_name=random_hex+f_ext
    path = os.path.join(app.root_path,'static/uploads_extra',new_name)
    pic.save(path)

    output_size=(200,200)
    i = Image.open(pic)
    i.thumbnail(output_size)
    i.save(path)
    return new_name

def get_products_from_session(session_cart):
    product_data = []
    for item in session_cart:
        product_id = item.get('productId')  # Adjust based on your actual data structure
        product = Product.get_or_404(product_id)
        if product:
            product_data.append(product)
    return product_data

def is_admin(user):
        return user.admin


def send_async_email(app, msg):
     with app.app_context():
          mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
     msg = Message(subject , sender=sender, recipients=recipients)
     msg.body = text_body
     msg.html = html_body
     Thread(target=send_async_email, args=(app,msg)).start()

def send_reset_request(user):
     token = user.get_reset_password_token()
     send_email('Eshop Password Reset',sender= 'kiplimo.antony@students.kyu.ac.ke',
                recipients=[user.email],
                text_body=render_template('email/reset_password.txt', user=user, token=token),
                html_body=render_template('email/reset_password.txt', user=user, token=token))
     

def send_payment_confirmation_email(user, orders):
     send_email('Eshop Payment Confirmation',sender= Config.ADMINS[0],
                recipients=[user.email],
                text_body=render_template('email/payment_confirmation.txt', user=user, orders=orders),
                html_body=render_template('email/payment_confirmation.html', user=user, orders=orders))
def merge_dicts(dict1,dict2):
    if isinstance(dict1,list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
         return dict(list(dict1.items()) + list(dict2.items()))
    else:
         return False