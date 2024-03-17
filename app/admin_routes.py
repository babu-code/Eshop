from flask_login import current_user, login_required, logout_user
from flask import Flask,abort, render_template, flash, redirect, url_for
from functools import wraps
from app.models import User, Product
from app.forms import AdminUserCreateForm
from app import db, app, bcrypt



def admin_login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_admin():
            return abort(403)
        return func(*args, **kwargs)
    return decorated_view


@app.route('/admin')
@login_required
@admin_login_required
def home_admin():
    return render_template('admin/admin-home.html')

@app.route('/admin/users_list')
@login_required
@admin_login_required
def users_list():
    users = User.query.all()
    return render_template('admin/users_list.html' ,users=users)

@app.route('/admin/create_user', methods=['GET',
 'POST'])
@login_required
@admin_login_required
def create_user():
    form = AdminUserCreateForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        admin = form.admin.data
        existing_username = User.query.filter_by(username=username).first()
        existing_email = User.query.filter_by(email=email).first()

        if existing_username:
            flash(
                'This username already exists. Try another one'
            )
            return redirect(url_for('create_user', form=form))
        if existing_email:
            flash(
                'This email already exists. Try another one'
            )
            return redirect(url_for('create_user', form=form))
        password_hash = bcrypt.generate_password_hash(password).decode()
        user = User(username,email, password_hash, admin)
        db.session.add(user)
        db.session.commit()
        flash('New User Created')
        return redirect(url_for('users_list'))
    if form.errors:
        flash(form.errors)
    return render_template('admin/create_user.html',form=form)

@app.route('/admin/delete_user/<int:user_id>', methods=['GET',
 'POST'])
@login_required
@admin_login_required
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        flash('User has been deleted')
        return redirect(url_for('users_list'))
    flash("User has been deleted")
    return redirect(url_for('users_list'))


@app.route('/admin/product_list', methods=['GET',
 'POST'])
@login_required
@admin_login_required
def product_list():
    products = Product.query.all()
    return render_template('admin/product_list.html', products=products)

@app.route('/admin/delete_product/<int:product_id>', methods=['GET',
 'POST'])
@login_required
@admin_login_required
def delete_product(product_id):
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        flash('Proudct has been deleted')
        return redirect(url_for('users_list'))
    flash("Product not found")
    return redirect(url_for('admin/product_list'))

