import secrets
from werkzeug.utils import secure_filename
from flask import Flask, request, render_template,abort, flash, redirect, url_for, session,jsonify,g, make_response
from app.models import Product, Category, User, CustomerOrder
from app.forms import ProductForm, CategoryForm, RegistrationForm, LoginForm, ResetPasswordRequestForm, ResetPasswordForm, EmptyForm, EditProfile,Checkout
from app import app,db, bcrypt
from flask_login import login_user,logout_user, login_required, current_user
from app.utils import save_pic, save_extra_pics, is_admin, send_reset_request, merge_dicts, send_payment_confirmation_email
import logging
from app.admin_routes import home_admin
import pdfkit
import openai
import bleach
import stripe
import requests
from requests.auth import HTTPBasicAuth
import base64
from datetime import datetime
import math
import random



my_endpoint = "https://d892-154-159-252-155.ngrok-free.app"


stripe.api_key="sk_test_51ObJVPKaiOXmNBGLUjSmzO92EHFOJ59VO8J0NIMexd5IL2PwT3Zp6x07pagC1z67d954XJbD0Bog5qUDHzj9qSw10032Q6HTgd"
publishable_key="pk_test_51ObJVPKaiOXmNBGLUpgwWHeuopC25YmcK4HQ1NLGlHhwl9CzGoi70NKWL2ztpN6SSiRbT8Db1lWg9XKGH6nsfK1y00fnTVwTpk"

try:
    path_wkhtmltopdf= b'C:\Program Files\wkhtmltopdf\\bin\wkhtmltopdf.exe'
    config=pdfkit.configuration(wkhtmltopdf = path_wkhtmltopdf)
    
    pdfkit.from_url("https://google.com", "order.pdf", configuration=config)
except Exception:
    print(Exception)

@app.route('/')
@app.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    products = Product.query.paginate(page=page, per_page=app.config['PER_PAGE'])
    best_deals = Product.query.order_by(Product.discount.desc()).paginate(page = page, per_page=app.config['PER_PAGE'])
    cheapest_products = Product.query.order_by(Product.price.asc()).paginate(page = page, per_page=app.config['PER_PAGE'])
    return render_template('home.html', products=products, page=page, best_deals=best_deals, cheapest_products=cheapest_products)

@app.route('/home/best_deals')
def best_deals():
    page = request.args.get('page', 1, type=int)
    best_deals = Product.query.order_by(Product.discount.desc()).paginate(page = page, per_page=app.config['PER_PAGE'])
    return render_template('home/best_deals.html',  products=best_deals)
@app.route('/home/latest_deals')
def latest_deals():
    page = request.args.get('page', 1, type=int)
    latest_products = Product.query.paginate(page = page, per_page=app.config['PER_PAGE'])
    return render_template('home/latest_deals.html',  products=latest_products)
@app.route('/home/cheapest_products')
def cheapest_products():
    page = request.args.get('page', 1, type=int)
    cheapest_deals = Product.query.order_by(Product.price.desc()).paginate(page = page, per_page=app.config['PER_PAGE'])
    return render_template('home/cheapest_products.html',  products=cheapest_deals)

@app.route('/register', methods=['GET','POST'])
def register():
    form= RegistrationForm()
    if form.validate_on_submit():
        password_hash=bcrypt.generate_password_hash(form.password.data).decode()
        user = User(username=form.username.data, email=form.email.data, password=password_hash,city = form.city.data,phone=form.phone.data, address=form.address.data )
        db.session.add(user)
        db.session.commit()
        flash ("Your Account has been created!")
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user= User.query.filter_by(email=form.email.data).first()
        print(user)
        if user and bcrypt.check_password_hash( user.password,form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            if user.is_admin():
                redirect(url_for('home_admin'))
            flash (f'Welcome @{user.username} !')
            return redirect(next_page) if next_page else redirect (url_for('home'))
        else:
            flash('Login Failed. Check your email and password')
            return redirect(url_for('login'))
    
    return render_template('login.html', form = form)

@app.route('/reset_password_request', methods=['GET','POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user:
            print(user)
            send_reset_request(user)
            flash('An email with instructions to reset your password has been sent to your email ')
    return render_template('reset_password_request.html', form=form)

@app.route('/reset_password/<token>')
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_password_token(token)
    if not user:
        flash("user doesnt exist")
        return redirect(url_for('home'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        print("Vlad")
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_pw
        print(hashed_pw)
        db.session.commit()
        flash('Your Password has been successfully changed')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)
    
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/profile/<string:username>')
@login_required
def profile(username):
    user=current_user
    form=EmptyForm()
    return render_template('profile.html', form=form, user=user)



@app.route('/profile/edit_profile',methods=['GET','POST'])
@login_required
def edit_profile():
    form=EditProfile(original_username=current_user.username)
    if form.validate_on_submit():
        current_user.username= form.username.data
        current_user.email=form.email.data
        current_user.city=form.city.data
        current_user.phone = form.phone.data
        current_user.address=form.address.data
        db.session.commit()
        flash('Your profile has been edited')
        return redirect(url_for('profile' ,username=current_user.username))
    
    elif request.method=='GET':
        form.username.data=current_user.username
        form.email.data= current_user.email
        if current_user.address:
            form.address.data=current_user.address
        
        if current_user.phone:
            form.phone.data = current_user.phone
        
        if current_user.city:
            form.city.data = current_user.city
        
        return render_template('edit_profile.html', form=form)


    


@app.route('/product/<id>', methods=['GET','POST'])
def product(id):
    product= Product.query.get_or_404(id)
    other_products_like_this = Product.query.filter_by(category_id = product.category.id).order_by(Product.discount.desc()).limit(8)
    category = product.category.query.filter_by(id=product.category_id).first()
    print(category)
    Prod = Product.query.filter_by(category_id = category.id).all()
    return render_template('product.html', product=product,random= random, category=category, Prod=Prod, other_products_like_this = other_products_like_this)

@app.route('/image/<name>')
def image(name):
    return redirect(url_for('static', filename='uploads/'+name))

@app.route('/image_extra/<name>')
def image_extra(name):
    return redirect(url_for('static', filename='uploads_extra/'+name))

@app.route('/create_product', methods=['POST', 'GET'])
@login_required
def create_product():
    form = ProductForm(meta={'csrf': False})
    categories = [(c.id, c.name) for c in Category.query.all()]
    print(categories)
    form.category.choices = categories

    if form.validate_on_submit():
        category=Category.query.get_or_404(
            form.category.data
        )
        if form.image.data :
            file_path=save_pic(form.image.data)
        img1=""
        img2=""
        img3=""
        img4=""
        if form.pic_1.data:
            img1=save_extra_pics(form.pic_1.data)
        
        if form.pic_2.data:
            img2=save_extra_pics(form.pic_2.data)
        
        if form.pic_3.data:
            img3=save_extra_pics(form.pic_3.data)
        
        if form.pic_4.data:
            img4=save_extra_pics(form.pic_4.data)
        
        
        product=Product(name=form.name.data,stock=form.stock.data, price=form.price.data,discount=form.discount.data ,description=form.description.data, category=category, image_path=file_path,
                    pic_1=img1, pic_2=img2, pic_3=img3, pic_4=img4  )
        db.session.add(product)
        db.session.commit()
        flash('Product has created')

        return redirect(url_for('home'))
        
    if form.errors:
        flash(form.errors)
    
    return render_template('create_products.html', form = form)
@app.route('/remove_product/<int:product_id>', methods=['GET','POST'])  
def remove_product(product_id):
     product = Product.query.get_or_404(product_id)
     db.session.delete(product)
     db.session.commit()
     flash('Product deleted!')
     return redirect(url_for('home'))
@app.route('/create_category', methods=['GET','POST'])
def create_category():
 form = CategoryForm()
 if form.validate_on_submit():
    category = Category(name=form.name.data)
    db.session.add(category)
    db.session.commit()
    flash('Category Created!')
    return redirect(url_for('home'))
 if form.errors:
     flash(form.errors)
 return render_template('create_category.html', form=form)

@app.template_filter('full_name')
def full_name_filter(product):
    return f"{product['category']}/ {product['name']}"

@app.route('/categories')
def categories():
    all_categories= Category.query.all()
    return render_template('categories.html', all_categories=all_categories)


@app.route('/category/<int:category_id>')
def category(category_id):
    category = Category.query.get_or_404(category_id)
    products = category.products
    return render_template('category.html', category=category, products=products) 
      
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    try:
        product_id= request.form.get("product_id")
        quantity=request.form.get('qty')
        product= Product.query.get_or_404(product_id)
        if product_id and quantity and request.method=='POST':
            dict_items= {product_id:{'name':product.name, 'price':product.price, 'discount': product.discount, 
                                     "quanitity":quantity, "image":product.image_path}}
            if 'shoppingCart'  in session:
                if product_id in session['shoppingCart']:
                    flash("Product already in cart")
                else:
                    session['shoppingCart'] = merge_dicts(session['shoppingCart'], dict_items)
                    flash("Product succesfully added to cart")
                    return redirect(url_for(request.referrer))
            else:
                session['shoppingCart'] = dict_items
                return redirect(url_for(request.referrer))
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)
@app.route('/clear_session', methods=['GET','POST'])
def clear_session():
    session['cart'].clear()
    session.modified = True
    flash('Session Deleted')
    return redirect(url_for('home'))

@app.route('/remove_from_session/<int:product_id>', methods=['POST'])
def remove_from_session(product_id):
    updated_cart = [item for item in session['cart'] if item.get('id') != product_id]
    session['cart'] = updated_cart
    session.modified=True
    updated_order = [item for item in session['items'] if item.get('id') != product_id]
    session['items'] = updated_order
    return redirect(url_for('view_cart'))

            
@app.route('/view_cart')
def view_cart():
    if 'shoppingCart' not in session or len(session['shoppingCart'])<=0:
        flash("The Cart is empty!")
        return redirect(url_for('home'))
    subtotal = 0
    grandtotal = 0
    for key, product in session['shoppingCart'].items():
        discount = (product['discount'])/100 *float(product['price'])
        subtotal +=float(product['price'])* int(product['quanitity'])
        subtotal -=discount
        tax = ("%.2f" % (.16 * subtotal))
        grandtotal = float("%.2f" % (1.16 * subtotal))
    return render_template('cart.html', tax=tax , grandtotal = grandtotal)
    

@app.route('/search')
def search():
    q = request.args.get('q')

    if q:
        results = Product.query.filter(Product.name.icontains(q)|Product.id.icontains(q))\
                                       .order_by(Product.name.desc())\
                                       .order_by(Product.id.asc()).limit(10)
    else:
        results=[]
    return render_template('search_results.html', results=results)




@app.route('/get_qty', methods=['post'])
def get_qty():
    session['total_amount'] = []
    id = request.form.get('qty-id')
    qty=request.form.get('qty')
    product= Product.query.get_or_404(id)
    item={"name":product.name, "price":product.price,"image_path":product.image_path, "id":product.id, "quantity":qty, "gross-price":(int(product.price) * int(qty))}

    existing_item = next((i for i in session['cart'] if i['id'] == item['id']), None)

    if existing_item:
        # Update quantity for the first matching item
        existing_item['quantity'] = qty
        cart_item = next((ci for ci in session['cart'] if ci['id'] == item['id']), None)
        if cart_item:
            cart_item['quantity']=qty
            cart_item['gross_price'] = (int(product.price)-(int(product.price)*int(product.discount)/100)) * int(qty)
            session.modified = True
    return redirect(url_for('view_cart'))


@app.route('/update_cart/<int:code>', methods=['GET','POST'])
def update_cart(code):
    if 'shoppingCart' not in session and len(session['shoppingCart']) <=0:
        return redirect(url_for('home'))
    if request.method=='POST':
        quantity = request.form.get('quantity')
        print("Quantity :",quantity)
        try:
            session.modified = True
            for key, item in session['shoppingCart'].items():
                if int(key) ==code:
                    item['quanitity'] = quantity
                    flash('Quantity succesfully updated')
                    return redirect(url_for('view_cart'))
        except Exception as e:
            print(e)
    return redirect(url_for('view_cart'))
@app.route('/remove_from_cart/<int:id>')
def remove_from_cart(id):
    if 'shoppingCart' not in session and len(session['shoppingCart']) <=0:
        return redirect(url_for('home'))
    try:
        session.modified=True
        for key,_ in session['shoppingCart'].items():
            if int(key) == id:
                session['shoppingCart'].pop(key)
                return redirect(url_for('view_cart'))
    except Exception as e:
        print(e)
        return redirect(url_for('view_cart'))
@app.route('/get_order')
@login_required
def get_order():
    if current_user.is_authenticated:
        customer_id = current_user.id
        invoice = secrets.token_hex(5)
        try:
            order = CustomerOrder(invoice=invoice, customer_id=customer_id, orders=session['shoppingCart'])
            db.session.add(order)
            db.session.commit()
            flash('Your order has been sent')
            return redirect(url_for('orders',invoice=invoice))
        except Exception as e:
            print( "Something went wrong while getting order")
            return redirect(url_for('view_cart'))
        
@app.route('/orders/<invoice>')
@login_required
def orders(invoice):
    if current_user.is_authenticated:
            
        grand_total = 0
        subtotal = 0
        customer_id = current_user.id
        customer = User.query.get_or_404(customer_id)
        orders =CustomerOrder.query.get_or_404(customer_id)
        for _key, product in orders.orders.items():
            discount = (product['discount']/100) * float(product['price'])
            subtotal +=float(product['price']) * int(product['quanitity'])
            subtotal-=discount
            tax = ("%.2f" % (.16 * float(subtotal)))
            grand_total = "%.2f" % (1.16 *float(subtotal))
    else:
        return redirect(url_for('login'))
    return render_template('orders.html', invoice=invoice, tax=tax, subtotal=subtotal, grand_total=grand_total, customer=customer, orders=orders)


@app.route('/payment', methods=['POST'])
@login_required
def payment():
    
    user=current_user
    invoice = request.form.get("invoice")
    amount = request.form.get("amount")
    customer = stripe.Customer.create(
    email=request.form['stripeEmail'],
    source=request.form['stripeToken'],
    )

    charge = stripe.Charge.create(
    customer=customer.id,
    description=invoice,
    amount=amount,
    currency='kes',
    )
    orders =CustomerOrder.query.filter_by(id=current_user.id,invoice=invoice).order_by(
        CustomerOrder.id.desc()).first()
    
    orders.status="Paid"
    db.session.commit()
    send_payment_confirmation_email(user,orders)
    flash("An Email with payment confirmation has been sent to you")
    return redirect(url_for('thanks'))

@app.route('/thanks')
def thanks():
    return render_template('thank.html')
@app.route('/get_pdf/<invoice>', methods=['GET','POST'])
@login_required
def get_pdf(invoice):
    if current_user.is_authenticated:
        grand_total = 0
        subtotal = 0
        customer_id = current_user.id
        if request.method=='POST':
            customer = User.query.get_or_404(customer_id)
            orders =CustomerOrder.query.get_or_404(customer_id)
            for _key, product in orders.orders.items():
                discount = (product['discount']/100) * float(product['price'])
                subtotal +=float(product['price']) * int(product['quanitity'])
                subtotal-=discount
                tax = ("%.2f" % (.16 * float(subtotal)))
                grand_total = float("%.2f" % (1.16 * subtotal))
            rendered= render_template('pdf.html', invoice=invoice, tax=tax,grand_total=grand_total, customer=customer, orders=orders)
            try:
                pdf = pdfkit.from_string(rendered, False )
                response = make_response(pdf)
                response.headers['content-Type'] = 'application/pdf'
                response.headers['content-Disposition'] = 'inline: filename=' + invoice + '.pdf'
                return response
            except Exception as e:
                print(e)
                flash("Something Went wrong")
    return redirect(url_for('orders', invoice=invoice ))

@app.route('/chat_gpt', methods=['GET','POST'])
def chat_gpt():
    if request.method=='POST':
        json_data = request.get_json()
        msg = bleach.clean(json_data.get("msg"))
        print(msg)
        openai.api_key = app.config['OPENAI_KEY']
        messages = [{
            "role": "system",
            "content": "You are a helpful chat assistant for a generic Ecommerce website"
        },
        {"role": "user", "content":msg}]

        response = openai.Completion.create(
            model = "gpt-3.5-turbo",
            messages=messages
        )

        return jsonify(
            message = response['choices'][0]['message']['content']
        )
    
    return render_template('chatgpt-demo.html')

# @app.route('/assistant', methods=['GET','POST'])
# def assistant():
#     if request.method =='POST':
#         inp = request.form.get('message')
#         query = inp
#         response = bot.chatbot.get_response(query)
#         return jsonify(message = response)
#     return render_template('assistant.html')

@app.route('/callback', methods=['POST'])
def incoming():
    data = request.get_json()
    print("Collected Json Data:",data)
    return "ok"
@app.route('/pay')
def mpesa_express():
    amt = request.args.get('total')
    am = float(amt)
    amount = math.ceil(am)
    phone_number = request.args.get('phone-number')
    endpoint= "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"    
    access_token = get_access_token()
    headers = {"Authorization" : f"Bearer {access_token}"}
    timestamp = datetime.now()
    times = timestamp.strftime("%Y%m%d%H%M%S")
    password = "174379"+"bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"+times
    password = base64.b64encode(password.encode('utf-8')).decode('utf-8')
   
    data = {
            "BusinessShortCode": "174379",
            "Password": password, 
            "Timestamp": times, 
            "TransactionType": "CustomerPayBillOnline",
            "PartyA": "254" + str(phone_number),
            "PartyB": "174379",
            "PhoneNumber":"254"+ str(phone_number),
            "CallBackURL": my_endpoint + "/callback",
            "AccountReference": "TestPay",
            "TransactionDesc": "HelloTest",
            "Amount":amount
            
        }
    
    try: 
        res = requests.post(endpoint, json = data, headers=headers)
        print(res.json())
        flash("Your payment is being processed. Check your email for payment details")
        return res.json()
    except ConnectionError as e:
        flash("Something went wrong. Please check your internet connection and try again")
        print(e)
        
    

def get_access_token():
    consumer_key = "UCeh468rOYGCcVEi3SEsBlSue84MZxvh2VpK1t6sN0sxGw6N"
    consumer_secret= "cSQbGVTAMBo9F7tPEGikM7GX2JNCntCcxYpDbsLiU8OouuO72JYze3v6AXHdGGPQ"
    endpoint = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    try:
        response = requests.get(endpoint, auth= HTTPBasicAuth(
            consumer_key, consumer_secret
        ))
        data = response.json()
        return data['access_token']
    except requests.exceptions.ConnectionError as e:
        flash("Something went wrong. Please check your internet connection and try again")
        print(e)
        return redirect(url_for('view_cart'))
    