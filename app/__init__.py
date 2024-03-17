import os
import logging
from flask import Flask,g
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from app.config import Config
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask_mail import Mail


app=Flask(__name__)
app.config.from_object(Config)
moment=Moment(app)
db=SQLAlchemy(app)
migrate=Migrate(app,db)
bcrypt= Bcrypt(app)
mail=Mail(app)
login_manager=LoginManager(app)
login_manager.login_view='login'

if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler= SMTPHandler(mailhost=(app.config['MAIL_SERVER'],app.config['MAIL_PORT']),
                    fromaddr='noreply@'+ app.config['MAIL_SERVER'],
                    toaddrs=app.config['ADMINS'],subject="Eshop Failure",
                    credentials=auth, secure=() )
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

    if not os.path.exists('logs'):
        os.mkdir('logs')
    filehandler = RotatingFileHandler('logs/Eshop.log',maxBytes=10240, backupCount=10)
    filehandler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    filehandler.setLevel(logging.INFO)
    app.logger.addHandler(filehandler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Eshop startup')
from app.models import Category, Product
    
@app.shell_context_processor
def make_shell_context():
    return {'app':app, 'db':db, 'Category':Category, 'Product':Product}

from app import routes, admin_routes, errors