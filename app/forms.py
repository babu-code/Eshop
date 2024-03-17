from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, DecimalField, SelectField, SubmitField, PasswordField, BooleanField, TextAreaField, IntegerField, HiddenField
from wtforms.validators import DataRequired, NumberRange, ValidationError, Length, Email, EqualTo
from app.models import Category, User
from flask_login import current_user


class RegistrationForm(FlaskForm):
    username=StringField('Username', validators=[DataRequired(), Length(min=2,max=20)])
    email= StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password= PasswordField('Confirm_Password', validators=[EqualTo('password')])
    phone = IntegerField('Phone',validators=[DataRequired()] )
    city = StringField('City', validators=[DataRequired()])
    address= StringField('Address', validators=[DataRequired()])
    submit= SubmitField('Submit')

class LoginForm(FlaskForm):
    email= StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember=BooleanField('Remember Me')
    submit= SubmitField('Submit')

class CategoryField(SelectField):

    def iter_choices(self):
        categories = [(c.id, c.name) for c in 
                      Category.query.all()]
        for value, label in categories:
            yield (value, label, self.coerce(value)==
                   self.data)
            
    # def pre_validate(self, form):
    #     for v, _ in [(c.id, c.name) for c in
    #                  Category.query.all()]:
    #         if self.data == v:
    #             break
    #         else:
    #             raise ValueError(self.gettext('Not a valid choice'))
       
      

class NameForm(FlaskForm):
    name = StringField('Name',
    validators=[DataRequired()])
            
class ProductForm(FlaskForm):
    name = StringField('Name',
    validators=[DataRequired()])
    price = DecimalField('Price', validators=[
        DataRequired(), NumberRange(min=0.0)
        ])
    stock = IntegerField("Stock", validators=[NumberRange(min=1)])
    discount= IntegerField("Discount", validators=[NumberRange(min=0, max=100)])
    category = CategoryField(
        'Category', validators=[DataRequired()],coerce=int)    
    image = FileField('Product Image',
        validators=[FileRequired(), FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=1,max=2000)])
    submit =  SubmitField('Submit')
    pic_1 = FileField('Picture 1',
        validators=[ FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])
    pic_2 = FileField('Picture 2',
        validators=[ FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])
    pic_3 = FileField('Picture 3',
        validators=[ FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])
    pic_4 = FileField('Picture 4',
        validators=[ FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])
    
def check_duplicate_category(case_sensitive=True):
    def _check_duplicate(form, field):
        if case_sensitive:
            res = Category.query.filter(
            Category.name.like('%' + field.data + '%')
            ).first()
        else:
            res = Category.query.filter(
            Category.name.ilike('%' + field.data + '%')
            ).first()
        if res:
            raise ValidationError(
                'Category named %s already exists' %
                    field.data
        )
    return _check_duplicate
class CategoryForm(NameForm):
 name = StringField('Name', validators=[
DataRequired(), check_duplicate_category()
 ])
class QuantityForm(FlaskForm):
     quantity = IntegerField("Quantity", validators=[DataRequired(), NumberRange(min=1)])
     hidden_field= HiddenField()

class AddToCartForm(FlaskForm):
    submit = SubmitField('+ Add To Cart')

class AdminUserCreateForm(FlaskForm):
    username = StringField('Username',
                    validators=[DataRequired()])
    email= StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired()])
    admin = BooleanField('Is Admin?')
    submit = SubmitField('Submit')

class AdminUserUpdateForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    admin = BooleanField('Is Admin?')

class ResetPasswordRequestForm(FlaskForm):
    email= StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')
class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password= PasswordField('Confirm New Password', validators=[EqualTo('password')])
    submit= SubmitField('Submit')

class EditProfile(FlaskForm):
    username=StringField('Username', validators=[DataRequired(), Length(min=2, max=8)])
    email=StringField('Email', validators=[DataRequired(), Email()])
    phone = IntegerField("Phone", validators=[DataRequired()])
    address=StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    submit=SubmitField('Update')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfile, self).__init__(*args, **kwargs)
        self.original_username= original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('This username has already been taken.Please choose a different one.')
    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user and user.email!= current_user.email:
            raise ValidationError('This email has already been taken. Please choose a different one')

class EmptyForm(FlaskForm):
    submit=SubmitField('Submit')


class Checkout(FlaskForm):
    city= SelectField('City', choices=[
                        ('NBI', 'Nairobi'), ('KMB', 'Kiambu'), ('MSA', 'Mombasa'), ('ELD', 'Eldoret'), ('NKR', 'Nakuru'), ('KSM', 'Kisumu'), ('GRS', 'Garissa'), ('MCS', 'Machakos'), ('NYI', 'Nyeri')])
    payment_type = SelectField('Payment Type', choices=[
                               ('MP', 'Mpesa'), ('CC', 'Credit Card')])
