from app import app,db, login_manager
from flask_login import UserMixin
from datetime import datetime
import json
import jwt
from time import time

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(20))
    email=db.Column(db.String(120))
    country = db.Column(db.String(20), default="Kenya")
    city = db.Column(db.String(20), default="Nairobi")
    phone = db.Column(db.Integer)
    password = db.Column(db.String(20))
    admin = db.Column(db.Boolean())
    address = db.Column(db.String(60))
   

    def __init__(self,username,email, password,city, phone, address,admin=False):
        self.username=username
        self.password=password
        self.email=email
        self.city = city
        self.phone =phone
        self.address = address
        self.admin = admin


    def is_admin(self):
        return self.admin
    
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
        {'reset_password':self.id, 'exp':time() + expires_in},
        app.config['SECRET_KEY'], algorithm='HS256')
    
    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return 
        return User.query.get(id)
    
class JsonEncodedDict(db.TypeDecorator):
    impl = db.Text
    def process_bind_param(self, value, dialect):
        if value is None:
            return '{}'
        else:
            return json.dumps(value)
    def process_result_value(self,value , dialect):
        if value is None:
            return {}
        else:
            return json.loads(value)
# class Order(db.Model):
#     id=db.Column(db.Integer, primary_key=True)
#     customer_id = db.Column(db.Integer, unique=False, nullable=False)

class CustomerOrder(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    invoice = db.Column(db.String(20), unique=True, nullable=False)
    status = db.Column(db.String(20), default='Pending' ,nullable=False)
    customer_id = db.Column(db.Integer, unique=False, nullable=False)
    date_created=db.Column(db.DateTime, default=datetime.utcnow)
    orders=db.Column(JsonEncodedDict )

    def __repr__(self):
        return f'<Customer Order {self.invoice}'


class Product(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(255))
    price=db.Column(db.Float)
    discount=db.Column(db.Float)
    stock= db.Column(db.Integer)
    
    

    category_id=db.Column(db.Integer, db.ForeignKey('category.id'))
    image_path = db.Column(db.String(255))

    pic_1 = db.Column(db.String(255), default='default.jpg')
    pic_2 = db.Column(db.String(255),default='default.jpg')
    pic_3 = db.Column(db.String(255),default='default.jpg')
    pic_4 = db.Column(db.String(255),default='default.jpg')
    description=db.Column(db.String(2000))


    def __init__(self, name, price, category, image_path,discount,stock, description,pic_1,pic_2,pic_3,pic_4):
        self.price=price
        self.name=name
        self.stock = stock
        self.category=category
        self.discount=discount
        self.image_path = image_path
        self.description=description
        self.pic_1=pic_1
        self.pic_2=pic_2
        self.pic_3=pic_3
        self.pic_4=pic_4
        

    def __repr__(self):
        return f'<Product( {self.id} name={self.name}, description={self.description})>'
    def selling_price(self):
        return self.price-(self.price*self.discount/100)

class Category(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100))
    products = db.relationship('Product', backref='category', lazy='dynamic')
    def __init__(self, name):
        self.name=name

    def __repr__(self):
        return f'<Category {self.name}>'
    
