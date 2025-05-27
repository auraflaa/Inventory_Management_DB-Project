from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
CORS(app)
csrf = CSRFProtect(app)

# Add flash message management
@app.before_request
def check_flash_messages():
    if request.path.endswith(('.js', '.css', '.ico', '.png', '.jpg', '.gif')):
        # Skip static files
        return
    # Check for suppress_flash cookie
    if request.cookies.get('suppress_flash'):
        session.pop('_flashes', None)  # Clear flash messages

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Pritam@127.0.0.1/inventory_management'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-123'  # In production, use a secure random key
app.config['WTF_CSRF_TIME_LIMIT'] = 3600  # 1 hour CSRF token expiry

from models import db

db.init_app(app)

# Import and register routes
from routes.product_routes import product_bp
from routes.admin_routes import admin_blueprint
from routes.customer_routes import customer_blueprint
from routes.order_routes import order_bp
from routes.other_routes import other_bp

app.register_blueprint(product_bp)
app.register_blueprint(admin_blueprint)  # url_prefix is already set in blueprint
app.register_blueprint(customer_blueprint, url_prefix='/customer')
app.register_blueprint(order_bp)
app.register_blueprint(other_bp)

# Home route (Customer Login Page)
@app.route('/')
def home():
    return render_template('index.html')

# API Endpoints for fetching data
@app.route('/api/products', methods=['GET'])
def get_products():
    # Fetch products from the database (mocked for now)
    products = [
        {"name": "Product A", "vendor": "Vendor X", "company": "Company Y", "details": "Details about Product A"},
        {"name": "Product B", "vendor": "Vendor Z", "company": "Company W", "details": "Details about Product B"}
    ]
    return jsonify(products)

@app.route('/api/orders', methods=['GET'])
def get_orders():
    # Fetch orders from the database (mocked for now)
    orders = [
        {"id": 1, "date": "2025-04-18", "status": "Shipped"},
        {"id": 2, "date": "2025-04-17", "status": "Processing"}
    ]
    return jsonify(orders)

@app.route('/api/customers', methods=['GET'])
def get_customers():
    # Fetch customers from the database (mocked for now)
    customers = [
        {"name": "John Doe", "email": "john@example.com", "phone": "123-456-7890"},
        {"name": "Jane Smith", "email": "jane@example.com", "phone": "987-654-3210"}
    ]
    return jsonify(customers)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('not_found.html'), 404

if __name__ == "__main__":
    app.run(debug=True)
