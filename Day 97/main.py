import os
from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from dotenv import load_dotenv
import stripe

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

from models import User, Product

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_first_request
def create_tables():
    db.create_all()
    # Seed some products if none exist
    if Product.query.count() == 0:
        items = [
            {'name': 'T-Shirt', 'price_cents': 2000},
            {'name': 'Mug', 'price_cents': 1500},
            {'name': 'Sticker', 'price_cents': 500},
        ]
        for it in items:
            db.session.add(Product(name=it['name'], price_cents=it['price_cents']))
        db.session.commit()

@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registered! Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/add_to_cart/<int:product_id>')
@login_required
def add_to_cart(product_id):
    cart = session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    session['cart'] = cart
    flash('Added to cart')
    return redirect(url_for('index'))

@app.route('/cart')
@login_required
def cart():
    cart = session.get('cart', {})
    items = []
    total = 0
    for pid, qty in cart.items():
        prod = Product.query.get(int(pid))
        items.append({'product': prod, 'quantity': qty})
        total += prod.price_cents * qty
    return render_template('cart.html', items=items, total=total)

@app.route('/create-checkout-session', methods=['POST'])
@login_required
def create_checkout_session():
    cart = session.get('cart', {})
    if not cart:
        flash('Cart is empty')
        return redirect(url_for('cart'))
    line_items = []
    for pid, qty in cart.items():
        prod = Product.query.get(int(pid))
        line_items.append({
            'price_data': {
                'currency': 'usd',
                'product_data': {'name': prod.name},
                'unit_amount': prod.price_cents,
            },
            'quantity': qty,
        })
    session.pop('cart')
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=url_for('success', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for('cart', _external=True),
    )
    return redirect(checkout_session.url, code=303)

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)
