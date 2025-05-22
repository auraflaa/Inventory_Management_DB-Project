from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session, flash
from models.customer import Customer
from models import db
from services.auth_service import verify_customer_login
from flask_wtf.csrf import CSRFError
from services.customer_service import get_customer_orders, get_customer_products
from models.product import Product
from models.order import Order
from models.order_detail import OrderDetail
from datetime import datetime

customer_bp = Blueprint('customer_routes', __name__, url_prefix='/api/customers')
customer_blueprint = Blueprint('customer', __name__)

@customer_bp.route('/', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    return jsonify([{
        "CustomerID": customer.CustomerID,
        "FirstName": customer.FirstName,
        "LastName": customer.LastName,
        "Email": customer.Email,
        "Phone": customer.Phone
    } for customer in customers])

@customer_bp.route('/<int:CustomerID>', methods=['GET'])
def get_customer(CustomerID):
    customer = Customer.query.get_or_404(CustomerID)
    return jsonify(customer.to_dict())

@customer_bp.route('/', methods=['POST'])
def create_customer():
    data = request.json
    new_customer = Customer(
        FirstName=data['FirstName'],
        LastName=data['LastName'],
        Email=data['Email'],
        Phone=data['Phone'],
        PasswordHash=data['PasswordHash']
    )
    db.session.add(new_customer)
    db.session.commit()
    return redirect(url_for('customer_dashboard'))

@customer_bp.route('/<int:CustomerID>', methods=['PUT'])
def update_customer(CustomerID):
    customer = Customer.query.get_or_404(CustomerID)
    data = request.json
    customer.FirstName = data['FirstName']
    customer.LastName = data['LastName']
    customer.Email = data['Email']
    customer.Phone = data['Phone']
    customer.PasswordHash = data['PasswordHash']
    db.session.commit()
    return jsonify(customer.to_dict())

@customer_bp.route('/<int:CustomerID>', methods=['DELETE'])
def delete_customer(CustomerID):
    customer = Customer.query.get_or_404(CustomerID)
    db.session.delete(customer)
    db.session.commit()
    return '', 204

# Customer Login Route
@customer_blueprint.route('/login', methods=['POST'])
def customer_login():
    try:
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            return render_template('index.html', error="Email and password are required")
            
        # Try to find a customer with matching email and password
        from services.auth_service import verify_password
        from models.customer import Customer
        customer = Customer.query.filter_by(Email=email).first()
        
        if customer and verify_password(password, customer.PasswordHash):
            return redirect(url_for('customer.customer_dashboard', customer_id=customer.CustomerID))
        
        return render_template('index.html', error="Incorrect email or password")
        
    except CSRFError:
        return render_template('index.html', error="Invalid form submission, please try again")

# Customer Dashboard Route
@customer_blueprint.route('/dashboard/<int:customer_id>', methods=['GET'])
def customer_dashboard(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    customer_name = f"{customer.FirstName} {customer.LastName}"
    products = get_customer_products(customer_id)
    orders = get_customer_orders(customer_id)
    return render_template('customer_dashboard.html', customer_name=customer_name, products=products, orders=orders, customer_id=customer_id, default_dark_mode=customer.DefaultDarkMode)

# Customer Orders Page Route
@customer_blueprint.route('/orders/<int:customer_id>', methods=['GET'])
def customer_orders_page(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    customer_name = f"{customer.FirstName} {customer.LastName}"
    orders = get_customer_orders(customer_id)
    return render_template('customer_orders.html', customer_name=customer_name, orders=orders, customer_id=customer_id)

# Customer Signup Route
@customer_blueprint.route('/signup', methods=['POST'])
def customer_signup():
    try:
        # Extract form data from the signup form
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')

        # Validate required fields
        if not all([first_name, last_name, email, phone, password]):
            return render_template('signup.html', error="All fields are required")

        # Check if the email is already registered
        if Customer.query.filter_by(Email=email).first():
            return render_template('signup.html', error="Email is already registered")

        # Create a new customer
        new_customer = Customer(
            FirstName=first_name,
            LastName=last_name,
            Email=email,
            Phone=phone,
            PasswordHash=password  # Store as plain text
        )    
        # Save the customer to the database
        db.session.add(new_customer)
        db.session.commit()

        # Redirect to the login page after successful signup
        return redirect(url_for('home'))
        
    except CSRFError:
        return render_template('signup.html', error="Invalid form submission, please try again")
    except Exception as e:
        db.session.rollback()
        return render_template('signup.html', error="An error occurred during signup. Please try again.")

@customer_blueprint.route('/signup', methods=['GET'])
def customer_signup_get():
    # Render the signup page for GET requests
    return render_template('signup.html')

@customer_blueprint.route('/all_customers', methods=['GET'])
def get_all_customers_for_debug():
    customers = Customer.query.all()
    return jsonify([
        {
            'CustomerID': c.CustomerID,
            'FirstName': c.FirstName,
            'LastName': c.LastName,
            'Email': c.Email,
            'Phone': c.Phone,
            'PasswordHash': c.PasswordHash
        } for c in customers
    ])

@customer_blueprint.route('/delete/<int:customer_id>', methods=['POST'])
def delete_customer_account(customer_id):
    import sys
    print(f"[DEBUG] Received request to delete customer {customer_id}", file=sys.stderr)
    try:
        customer = Customer.query.get_or_404(customer_id)
        print(f"[DEBUG] Found customer: {customer.CustomerID}", file=sys.stderr)
        db.session.delete(customer)
        db.session.commit()
        print(f"[DEBUG] Successfully deleted customer {customer_id}", file=sys.stderr)
        return redirect(url_for('customer.customer_account_deleted', success=1))
    except Exception as e:
        db.session.rollback()
        print(f"[ERROR] Exception while deleting customer {customer_id}: {e}", file=sys.stderr)
        return redirect(url_for('customer.customer_account_deleted', success=0))

@customer_blueprint.route('/account-deleted')
def customer_account_deleted():
    from flask import request
    success = request.args.get('success', '0')
    return render_template('account_deleted.html', success=success)

@customer_blueprint.route('/order', methods=['POST'])
def place_order():
    try:
        # CSRF validation happens automatically via Flask-WTF
        product_id = request.form.get('product_id')
        quantity = int(request.form.get('quantity', 1))
        customer_id = request.args.get('customer_id') or request.form.get('customer_id')
        print(f"[DEBUG] product_id={product_id}, quantity={quantity}, customer_id={customer_id}")
        product = Product.query.get(product_id)
        print(f"[DEBUG] product={product}")
        if not product:
            print("[ERROR] Product not found")
            return redirect(url_for('customer.customer_dashboard', customer_id=customer_id, error='Product not found.'))
        print(f"[DEBUG] product.QuantityPerUnit={product.QuantityPerUnit}")
        if int(product.QuantityPerUnit) < quantity:
            print("[ERROR] Not enough stock")
            return redirect(url_for('customer.customer_dashboard', customer_id=customer_id, error='Not enough stock.'))
        # Set principal employee id (e.g., 1)
        principal_employee_id = 1
        # Create order
        order = Order(
            EmployeeID=principal_employee_id,
            CustomerID=customer_id,
            OrderDate=datetime.now(),
            ShippedDate=None,
            OrderStatusID=1,  # Assuming 1 is 'Pending'
            PaymentMethod='N/A'
        )
        db.session.add(order)
        db.session.flush()  # Get order.OrderID
        # Create order detail
        order_detail = OrderDetail(
            OrderID=order.OrderID,
            ProductID=product_id,
            Quantity=quantity,
            UnitPrice=product.UnitPrice,
            Discount=0
        )
        db.session.add(order_detail)
        # Decrease product quantity
        product.QuantityPerUnit = str(int(product.QuantityPerUnit) - quantity)
        db.session.commit()
        print("[DEBUG] Order placed successfully")
        return redirect(url_for('customer.customer_dashboard', customer_id=customer_id, success='1'))
    except Exception as e:
        import traceback
        print("[ERROR] Exception in place_order:")
        print(traceback.format_exc())
        return redirect(url_for('customer.customer_dashboard', customer_id=request.args.get('customer_id') or request.form.get('customer_id'), error='Internal server error.'))

@customer_blueprint.route('/order/<int:order_id>', methods=['GET'])
def customer_order_details(order_id):
    from models.order import Order
    from models.order_detail import OrderDetail
    from models.product import Product
    from models.company import Company
    from models.product_vendor import ProductVendor
    order = Order.query.get_or_404(order_id)
    order_details = OrderDetail.query.filter_by(OrderID=order_id).all()
    detailed_products = []
    for detail in order_details:
        product = Product.query.get(detail.ProductID)
        vendor_name = 'N/A'
        company_name = 'N/A'
        product_vendor = ProductVendor.query.filter_by(ProductID=product.ProductID).first()
        if product_vendor:
            company = Company.query.get(product_vendor.VendorID)
            if company:
                vendor_name = company.CompanyName
                company_name = company.CompanyName
        detailed_products.append({
            'ProductName': product.ProductName if product else 'N/A',
            'CompanyName': company_name,
            'VendorName': vendor_name,
            'Quantity': detail.Quantity,
            'UnitPrice': detail.UnitPrice
        })
    return render_template('customer_order_details.html', order=order, products=detailed_products)

@customer_blueprint.route('/order/<int:order_id>/cancel', methods=['POST'])
def cancel_order(order_id):
    try:
        from models.order import Order
        from models.order_detail import OrderDetail
        from models.product import Product
        order = Order.query.get_or_404(order_id)
        # Restore product quantities
        order_details = OrderDetail.query.filter_by(OrderID=order_id).all()
        for detail in order_details:
            product = Product.query.get(detail.ProductID)
            if product:
                product.QuantityPerUnit = str(int(product.QuantityPerUnit) + detail.Quantity)
            db.session.delete(detail)
        db.session.delete(order)
        db.session.commit()
        flash("Order canceled successfully", "success")
        return redirect(url_for('customer.customer_orders_page', customer_id=order.CustomerID))
    except CSRFError:
        flash("Invalid form submission, please try again", "error")
        return redirect(url_for('customer.customer_order_details', order_id=order_id))
    except Exception as e:
        db.session.rollback()
        flash("An error occurred while canceling the order", "error")
        return redirect(url_for('customer.customer_order_details', order_id=order_id))

@customer_blueprint.route('/settings/<int:customer_id>', methods=['GET', 'POST'])
def customer_settings(customer_id):
    try:
        from models.customer import Customer
        customer = Customer.query.get_or_404(customer_id)
        if request.method == 'POST':
            dark_mode = request.form.get('default_dark_mode') == 'on'
            customer.DefaultDarkMode = dark_mode
            db.session.commit()
            flash("Settings updated successfully", "success")
            return redirect(url_for('customer.customer_settings', customer_id=customer_id))
        return render_template('customer_settings.html', customer=customer)
    except CSRFError:
        flash("Invalid form submission, please try again", "error")
        return redirect(url_for('customer.customer_settings', customer_id=customer_id))
    except Exception as e:
        db.session.rollback()
        flash("An error occurred while saving settings", "error")
        return redirect(url_for('customer.customer_settings', customer_id=customer_id))

@customer_blueprint.route('/account/<int:customer_id>', methods=['GET', 'POST'])
def update_account(customer_id):
    try:
        from models.customer import Customer
        customer = Customer.query.get_or_404(customer_id)
        if request.method == 'POST':
            customer.FirstName = request.form.get('first_name', customer.FirstName)
            customer.LastName = request.form.get('last_name', customer.LastName)
            customer.Email = request.form.get('email', customer.Email)
            customer.Phone = request.form.get('phone', customer.Phone)
            db.session.commit()
            flash("Account information updated successfully", "success")
            return redirect(url_for('customer.customer_settings', customer_id=customer_id))
        return render_template('customer_update_account.html', customer=customer)
    except CSRFError:
        flash("Invalid form submission, please try again", "error")
        return redirect(url_for('customer.update_account', customer_id=customer_id))
    except Exception as e:
        db.session.rollback()
        flash("An error occurred while updating account information", "error")
        return redirect(url_for('customer.update_account', customer_id=customer_id))

@customer_blueprint.route('/signout')
def customer_signout():
    # Clear any session data if needed
    session.clear()
    # Render the signout page
    return render_template('customer_signout.html')