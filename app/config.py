import os



basedir=os.path.abspath(os.path.dirname(__file__))


class Config():
    SECRET_KEY = 'yOU_CAN_NEVer_guess_it'
    SQLALCHEMY_DATABASE_URI='sqlite:///'+ os.path.join(basedir, 'app.db')
    PER_PAGE=4
    MAIL_SERVER=  'smtp.googlemail.com' #'localhost'
    MAIL_PORT= 587 #8025
    MAIL_USE_TLS=1
    MAIL_USERNAME=os.environ.get('MAIL_USERNAME') or 'kiplimo.antony@students.kyu.ac.ke'
    MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD') or 'sijui$$$'
    ADMINS=['kiplimo.antony@students.kyu.ac.ke','tonnieblair12@gmail.com']
    WKHTMLTOPDF_PATH = r'C:\Program Files\wkhtmltopdf.exe'
    OPENAI_KEY = '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'
    STRIPE_PUBLISHABLE_KEY = 'pk_test_TYooMQauvdEDq54NiTphI7jx'
    STRIPE_SECRET_KEY='sk_test_51ObJVPKaiOXmNBGLUjSmzO92EHFOJ59VO8J0NIMexd5IL2PwT3Zp6x07pagC1z67d954XJbD0Bog5qUDHzj9qSw10032Q6HTgd'